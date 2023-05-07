from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
from django.views.generic.list import ListView


class File(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    date_uploaded = models.DateField(default=datetime.datetime.now)
    file = models.FileField(upload_to='local_storage',default="")
    number_of_emails = models.IntegerField(default=0)
    number_of_downloads = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title 

    