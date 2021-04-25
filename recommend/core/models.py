from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    """ Time Stamped Model """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AbstractItem(TimeStampedModel):
    """ Abstract Item """
    name = models.CharField(max_length=80)
    class Meta:
        abstract = True

    def __str__(self):
        return self.name   
