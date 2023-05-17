from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    def __str__(self):
        return self.email


# CustomUser._meta.get_fields('email',include_parents=False)[0]._unique=True