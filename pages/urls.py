from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('update/', views.update),
    path('new/<str:type>', views.newUser),
    path('new', views.new),
    path('home', views.decidehome),
    path('denied/', views.denied),
    path('student/home', views.studentHome),
    path('teacher/home', views.teacherHome),
    path('logout/', views.logout_request),
    path('profile/edit', views.editProfile),
    path('profile/password/change', views.change_password),
    path('profile/password/change/<pass_1>/<pass_2>', views.change_password_2),
    path('about', views.about),
    path('site/map', views.site_map),
]