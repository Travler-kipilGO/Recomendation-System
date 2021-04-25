from django.urls import path
from . import views

app_name = "travels"

urlpatterns = [
    path('home/',  views.home,    name='home'),
    path('n_map/',  views.n_map,    name='n_map'),
]


