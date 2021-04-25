from django.contrib import admin 
from . import models 

# Register your models here. 
@admin.register(models.TravelSpot) 
class TravelSpotAdmin(admin.ModelAdmin): 
    pass

@admin.register(models.MyTripData)
class MyTripDataAdmin(admin.ModelAdmin): 
    pass

@admin.register(models.TravelRating)
class TravelRatingAdmin(admin.ModelAdmin): 
    pass


@admin.register(models.UserLogData)
class UserLogDataCodeAdmin(admin.ModelAdmin): 
    pass

@admin.register(models.CodeData)
class CodeDataAdmin(admin.ModelAdmin): 
    pass

@admin.register(models.ClassificationCode)
class ClassificationCodeAdmin(admin.ModelAdmin): 
    pass

