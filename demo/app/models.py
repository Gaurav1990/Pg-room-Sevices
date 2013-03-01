# Create your models here.
from django.db import models
from django.contrib.auth.models import User

AREA = (
    ('BTM', 'BTM'),
    ('ITPL', 'ITPL'),
    ('EC', 'EC'),
)


SHARE = (
    ('1 Sharing', '1 Sharing'),
    ('2 Sharing', '2 Sharing'),
    ('3 Sharing', '3 Sharing'),
)


FOOD = (
    ('Veg', 'Veg'),
    ('Non-Veg', 'Non- Veg'),
  
)

TYPE = (
    ('owner', 'owner'),
    ('seeker', 'seeker'),
  
)

RATE = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
  
)

class Pg(models.Model):
    area = models.CharField(max_length=50)
    total = models.IntegerField()
    #ads = models.ForeignKey(Ad)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    #re-password = models.CharField(max_length = 10)
    address = models.CharField( max_length = 10)
    user_type = models.CharField(max_length=10, choices = TYPE)


class Ad(models.Model):
    posted_by = models.CharField(max_length = 50)
    phn_no = models.IntegerField()    
    area = models.CharField(max_length=10, choices = AREA)
    monthly_rent = models.IntegerField()
    sharing = models.CharField(max_length=10, choices = SHARE)
    cuisine = models.CharField(max_length=10, choices = FOOD)

class Rating(models.Model):
    posted_by = models.CharField(max_length = 30)
    rating = models.CharField(max_length=10, choices = RATE)
    suggesion = models.TextField()
