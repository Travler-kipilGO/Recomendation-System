from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.
class PhotoInline(admin.TabularInline):
    model = models.Photo

@admin.register(models.Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)

    list_display = (
        "name",
        "country",
        "city",
    )
