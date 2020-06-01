from django.db import models
from classes.models import Class
from classes.models import class_linker
from django.contrib.auth.models import User

class Model_assignment(models.Model):
    name = models.CharField(max_length=120, blank = True)
    description = models.TextField(blank = True)
    linked_class = models.ForeignKey(Class, on_delete=models.CASCADE, blank = True, null = True)
    linked_teacher = models.ForeignKey(User ,on_delete=models.CASCADE, blank = True, null = True)

    def __str__(self):
        return (self.name + " (" +  self.linked_class.name + ")")

# Create your models here.
class Assignment(models.Model):
    name = models.CharField(max_length = 120)
    description = models.TextField()
    linked_class = models.ForeignKey(Class, on_delete=models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User ,on_delete=models.CASCADE, blank = True, null = True)
    done = models.BooleanField(default = False)
    linked_model_assignment = models.ForeignKey(Model_assignment, on_delete=models.CASCADE, blank = True, null = True)
    linked_class_linker = models.ForeignKey(class_linker, on_delete=models.CASCADE, blank = True, null = True)
    submission = models.TextField(default="")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return (self.name + " (" + self.user.first_name + ")")