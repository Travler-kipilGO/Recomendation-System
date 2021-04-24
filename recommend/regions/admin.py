from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Country, models.City)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """
    list_display = ("name",)