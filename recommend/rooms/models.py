from django.db import models
from core.models import TimeStampedModel
from accommodations.models import Accommodation
# Create your models here.
class Room(TimeStampedModel):
    """ Room Model Definition """
    accommodation = models.ForeignKey(Accommodation, related_name="rooms", on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    description = models.TextField(null=True)
    price = models.IntegerField(null=True)
    guests = models.IntegerField(null=True)    

    def __str__(self):
        return self.name
