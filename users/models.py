from django.db import models
# from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
    	return self.user, "Profile"