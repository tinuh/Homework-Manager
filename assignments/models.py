from django.db import models
from classes.models import Class
from django.contrib.auth.models import User

class Model_assignment(models.Model):
    name = models.CharField(max_length=120, blank = True)
    description = models.TextField(blank = True)
    linked_class = models.ForeignKey(Class, on_delete=models.CASCADE, blank = True, null = True)
    linked_teacher = models.ForeignKey(User ,on_delete=models.CASCADE, blank = True, null = True)

# Create your models here.
class Assignment(models.Model):
    name   = models.CharField(max_length = 120)
    description = models.TextField()
    linked_class = models.ForeignKey(Class, on_delete=models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User ,on_delete=models.CASCADE, blank = True, null = True)
    done = models.BooleanField(default = False)
    linked_model_assignment = models.ForeignKey(Model_assignment, on_delete=models.CASCADE, blank = True, null = True)

    def __unicode__(self):
        return self.name