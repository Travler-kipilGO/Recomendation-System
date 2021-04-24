from django.db import models
from core.models import TimeStampedModel
from django.utils import timezone
# Create your models here.

class Photo(TimeStampedModel):
    """ 사진 """
    thumb_img_src = models.TextField()
    img_src = models.TextField()
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)

# Create your models here.
class Accommodation(TimeStampedModel):
    """ 숙박 업소 """
    name = models.CharField(max_length=140)
    description = models.TextField() 
    country = models.ForeignKey("regions.Country", on_delete=models.SET_NULL, null=True) 
    city = models.ForeignKey("regions.City", on_delete=models.SET_NULL, null=True) 
    address = models.TextField()
    main_img_src = models.TextField()

    def __str__(self):
        return self.name
