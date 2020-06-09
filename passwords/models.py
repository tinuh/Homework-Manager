from django.db import models
from django.contrib.auth.models import User
from random import choice
import uuid

# Create your models here.
class ResetPWD(models.Model):
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=300)
    code = models.CharField(default=uuid.uuid4, unique=True, max_length=300)

    def __str__(self):
        return self.user.first_name