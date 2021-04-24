
from django.urls import path
from . import views

app_name = "accommodations"

urlpatterns = [
    path("", views.AccommodationView.as_view(), name="home"),
    path("<int:pk>/", views.AccommodationDetail.as_view(), name="detail"),
]