from django.db import models

# Create your models here.


class CodeData(models.Model):
    code_id = models.CharField(max_length=20)
    code_info = models.CharField(max_length=20)
    code_from = models.CharField(max_length=20)

    def __str__(self):
        return self.code_info    

class ClassificationCode(models.Model):
    contenttypeid = models.CharField(max_length=20)
    cat1 = models.CharField(max_length=20)
    cat1_name = models.CharField(max_length=20)
    cat2 = models.CharField(max_length=20)
    cat2_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.cat1_name + ',' + self.cat2_name
  

class TravelSpot(models.Model):
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

class MyTripData(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE) 
    travelspot = models.ForeignKey('TravelSpot', on_delete=models.CASCADE) 

    def __str__(self):
        return self.user.username + '-' + self.travelspot.title

class TravelRating(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE) 
    mytripdata   = models.ForeignKey('MyTripData', on_delete=models.CASCADE) 
    rating       = models.IntegerField()

    def __str__(self):
        return self.user.username + ',' + self.mytripdata.travelspot.title  +',' + str(self.rating)

class UserLogData(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    travelspot = models.ForeignKey('TravelSpot', on_delete=models.CASCADE) 
    click = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return self.user.username + ',' + self.travelspot.title  +',' + str(self.click)