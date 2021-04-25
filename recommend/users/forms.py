from django import forms 
from . import models

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput( attrs={"placeholder": "이메일"}))
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    def clean(self): 
        email = self.cleaned_data.get("email") 
        password = self.cleaned_data.get("password") 
        try: 
            user = models.User.objects.get(username=email) 
            if user.check_password(password): 
                return self.cleaned_data 
            else: 
                self.add_error("password", forms.ValidationError("Password is wrong")) 
        except models.User.DoesNotExist: 
                self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email Name"})
        }
        labels = {
            'first_name' : '이름',
            "last_name" : '성',
            "email" : '이메일'
        }
    password = forms.CharField(
        label='패스워드',
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        label='패스워드 확인',
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )
    age = forms.CharField(
        label='나이',
        widget=forms.TextInput(attrs={"placeholder": "나이"})
    )
    phone = forms.CharField(
        label='연락처',
        widget=forms.TextInput(attrs={"placeholder": "연락처"})
    )
    
    sex = forms.CharField(
        label='성별',
        widget=forms.Select(choices=models.sex_choice)
    )
    address = forms.CharField(
        label='주소',
        widget=forms.Select(choices=models.address_choice)
    )


    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password


    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        sex = self.cleaned_data.get("sex")
        phone = self.cleaned_data.get("phone")
        age = self.cleaned_data.get("age")
        address = self.cleaned_data.get("address")
        user.username = email
        user.sex = sex
        user.phone = phone
        user.address = address
        user.age = age
        user.set_password(password)
        user.save()

