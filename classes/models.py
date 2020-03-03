from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Class(models.Model):
    name   = models.CharField(max_length = 120)
    description = models.TextField()
    code = models.CharField(max_length=6)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)

    def __unicode__(self):
        return self.name

class class_linker(models.Model):
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    linked_user = models.ForeignKey(User, on_delete=models.CASCADE)