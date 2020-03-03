from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('student/view', views.studentClass),
    path('teacher/view', views.teacherClass),
    path('view', views.view),
    path('teacher/view/<int:id>', views.teacherSpecificClass),
    path('student/view/<int:id>', views.studentSpecificClass),
    path('add', views.class_add),
    path('student/join', views.join_class),
    path('delete/<int:id>', views.delete),
    path('remove/student/<int:class_id>/<int:user_id>', views.remove_student)
]