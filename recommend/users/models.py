from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse

# Create your models here.
class User(AbstractUser):
    """ Custom User Model """

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})