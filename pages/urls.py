from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('update/', views.update),
    path('new/<str:type>', views.newUser),
    path('new', views.new),
    path('home', views.home),
    path('denied/', views.denied),
    path('logout/', views.logout_request),
    path('about', views.about),
    path('site/map', views.site_map),
]