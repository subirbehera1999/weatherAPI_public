from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class History(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    city=models.CharField(max_length=50)
    date=models.DateField()
    time=models.CharField(max_length=20)