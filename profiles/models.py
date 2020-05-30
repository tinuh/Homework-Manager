from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.BooleanField(default = False)

    def __str__(self):
        if self.teacher:
            return ("*" + self.user.first_name)
        else:
            return (self.user.first_name)