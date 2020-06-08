from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('student/view', views.student),
    path('teacher/view', views.teacher),
    path('view', views.view),
    path('edit/<id>', views.edit),
    path('teacher/view/<int:id>', views.teacher_view),
    path('student/view/<int:id>', views.student_view),
    path('add', views.add),
    path('student/join', views.join),
    path('delete/<int:id>', views.delete),
    path('remove/student/<int:class_id>/<int:user_id>', views.remove_student)
]