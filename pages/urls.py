from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('update/', views.update),
    path('set/type/', views.new),
    path('new/', views.newUser),
    path('new/<type>', views.newUser),
    path('home/', views.home),
    path('denied/', views.denied),
    path('logout/', views.logout_request),
    path('about', views.about),
    path('site/map', views.site_map),
]