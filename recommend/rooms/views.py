from django.shortcuts import render
from django.views.generic import DetailView
from . import models
# Create your views here.


class RoomDetail(DetailView):
    """ RoomDetail Definition """
    model = models.Room

