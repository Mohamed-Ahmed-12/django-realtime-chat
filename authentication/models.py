from django.db import models

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
	pic = models.ImageField(upload_to='pic',default='defualt.jpeg')
	is_online = models.BooleanField(verbose_name='Online user', default=False)

