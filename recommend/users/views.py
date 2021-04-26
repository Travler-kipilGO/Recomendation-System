from django.views.generic import FormView, DetailView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.views import PasswordChangeView
from . import forms, models
import core.recommend as recommend
import core.friend as friend
import core.userlog as userlog
from accommodations.models import Accommodation
from reviews.models import Review
from travels.models import ClassificationCode

# Create your views here.


from django.views.generic import FormView 
from django.urls import reverse_lazy

class LoginView(FormView): 
    template_name = "users/login.html" 
    form_class = forms.LoginForm 

    def form_valid(self, form): 
        email = form.cleaned_data.get("email") 
        password = form.cleaned_data.get("password") 
        user = authenticate(self.request, username=email, password=password)
        if user is not None: 
            login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")

def log_out(request): 
    logout(request) 
    return redirect(reverse("core:home"))


class SignupView(FormView):
    template_name = "users/signup.html" 
    form_class = forms.SignUpForm 
    success_url = reverse_lazy("users:survey")

    def form_valid(self, form): 
        form.save() 
        email = form.cleaned_data.get("email") 
        password = form.cleaned_data.get("password") 
        user = authenticate(self.request, username=email, password=password) 
        if user is not None: 
            login(self.request, user) 
        return super().form_valid(form)

class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"
    
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user = models.User.objects.get(pk=self.kwargs['pk'])
        #recommends = recommend.get_k_neighbors(user.username, 3)
        #context['recommends'] = (
        #    Accommodation.objects.get(name=recommends[0]),
        #    Accommodation.objects.get(name=recommends[1]),
        #    Accommodation.objects.get(name=recommends[2])
        #)

        surveys = models.Survey.objects.filter(user=user)
        themes = []

        for survey in surveys:
            themes.append(ClassificationCode.objects.get(cat2=survey.theme))    
        context['themes'] = themes

        friendList = []
        friends = friend.main(user.username)
        for _, name in friends:
            print(name)
            friendList.append(models.User.objects.get(username=name))
            
        #print(friends[0][1])
        context['friends'] = friendList
        context['reviews'] = Review.objects.filter(user=user)
        return context


class UpdateProfileView(UpdateView):
    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "first_name",
        "last_name",
    )    

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        return form

class UpdatePasswordView(PasswordChangeView): 
    template_name = "users/update-password.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form
        
    def get_success_url(self):
        return self.request.user.get_absolute_url()


class SurveyView(View):
    def get(self, request):
        return render(request, 'users/survey.html')

    def post(self,request):
        return render(request, 'users/recommend.html')

class RecommendView(View):
    def get(self, request):
        username = request.user.username
        context = {}  
        recdata_list = []
        if username != '' and username != 'admin':
            recDatas = userlog.main(username)
            for recdata in recDatas:

                recdata_list.append(recdata[1])
            
            context['recdatas'] = recdata_list
            print(recdata_list)
        return render(request, 'users/recommend.html', context)

    def post(self,request):
        themes = request.POST.getlist('answer[]')
        for theme in themes:
            surveys = models.Survey(theme=theme, user=request.user)
            surveys.save()
        return render(request, 'users/recommend.html')    

    

def search(request) :
    return render(request, 'users/search.html')