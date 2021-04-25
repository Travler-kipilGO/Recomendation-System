from django.db import models

# # Create your models here.
# class Search(models.Model):
#     user_id         = models.AutoField()    # User_ID
#     area_code       = models.AutoField()    # 지역코드
#     tour_list       = models.AutoField()    # 관광지    추천리스트
#     culture_list    = models.AutoField()    # 문화시설  추천리스트
#     festival_list   = models.AutoField()    # 축제공연  추천리스트
#     leports_list    = models.AutoField()    # 레포츠    추천리스트
#     stay_list       = models.AutoField()    # 숙박      추천리스트
#     shopping_list   = models.AutoField()    # 쇼핑      추천리스트
#     restaurant_list = models.AutoField()    # 음식점    추천리스트

#     def __str__(self):
#         return self.user_id+", "+self.area_code+", "+self.tour_list

class Tour_spot(models.Model):
    areacode     = models.IntegerField()
    cat1         = models.CharField(max_length=100)
    cat2         = models.CharField(max_length=100)
    content_id   = models.IntegerField()
    content_type = models.IntegerField()
    mapx         = models.FloatField()
    mapy         = models.FloatField()
    readcount    = models.IntegerField()
    title        = models.CharField(max_length=100)

    def __str__(self):
        return self.cat1+", "+self.cat2+", "+self.title

class Tour_spot_rating(models.Model):
    user_id      = models.CharField(max_length=100)
    content_id   = models.IntegerField()
    rating       = models.FloatField()
    content_type = models.IntegerField()
    
    def __str__(self):
        return self.title
