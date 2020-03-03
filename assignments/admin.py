from django.contrib import admin
from .models import Assignment
from .models import Model_assignment

# Register your models here.

admin.site.register(Assignment)
admin.site.register(Model_assignment)
