from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
]
