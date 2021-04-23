from django.contrib import admin
from django.urls import path, include
from Map    import views

urlpatterns = [
    path('index/',  views.index,    name='index'),
    path('n_map/',  views.n_map,    name='n_map'),
    
]