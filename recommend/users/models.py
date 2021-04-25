from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse

# Create your models here.

class Survey(models.Model) :
    """ 설문 조사 """
    user = models.ForeignKey(
        "users.User", related_name="surveys", on_delete=models.CASCADE
    )
    theme   = models.CharField(max_length=10, verbose_name='테마')

    def __str__(self):
        return self.user.username+" , " + self.theme

address_choice = {
    ('1', '서울'),
    ('2', '인천'),
    ('3', '대전'),
    ('4', '대구'),
    ('5', '광주'),
    ('6', '부산'),
    ('7', '울산'),
    ('8', '세종특별자치시'),
    ('31', '경기도'),
    ('32', '강원도'),
    ('33', '충청북도'),
    ('34', '충청남도'),
    ('35', '경상북도'),
    ('36', '경상남도'),
    ('37', '전라북도'),
    ('38', '전라남도'),
    ('39', '제주도'),
}

sex_choice = {
    ('S01', '남자'),
    ('S02', '여자'),
}


class User(AbstractUser):
    """ Custom User Model """

    sex     = models.CharField(default='S01', max_length=10, verbose_name='성별', choices=sex_choice)
    age     = models.CharField(null=True, max_length=10, verbose_name='나이')
    phone   = models.CharField(null=True, max_length=20, verbose_name='전화번호')
    address = models.CharField(default='1', max_length=10, verbose_name='주소', choices=address_choice)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})