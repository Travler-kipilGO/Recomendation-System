from django.db import models
from core.models import AbstractItem

# Create your models here.
class Country(AbstractItem):
    """ 나라 """
    def __str__(self):
        return f'{self.name}'

class City(AbstractItem):
    """ 도시 """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return f'{self.name}'