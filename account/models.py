from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class user_profile_info(models.Model):
        user = models.OneToOneField(User, on_delete = models.CASCADE)
        profolio_site = models.URLField(blank = True, default='#')
        profile_pic = models.ImageField(upload_to = 'profile_pics',blank = True, default='#')

        def __str__(self):
            return self.user.username
