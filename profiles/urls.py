from django.urls import path
from . import views

urlpatterns = [
    path("edit/", views.edit),
    path('password/change', views.change_password),
]