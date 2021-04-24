from django.urls import path
from accommodations import views as accommodation_views

app_name = "core"

urlpatterns = [path("", accommodation_views.AccommodationView.as_view(), name="home")]