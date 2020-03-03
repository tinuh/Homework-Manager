from django.contrib import admin
from .models import Class
from .models import class_linker

# Register your models here.

admin.site.register(Class)
admin.site.register(class_linker)