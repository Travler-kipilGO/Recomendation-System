from django.contrib import admin 
from . import models 

# Register your models here. 
@admin.register(models.User) 
class CustomUserAdmin(admin.ModelAdmin): 
    pass

@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin): 
    pass