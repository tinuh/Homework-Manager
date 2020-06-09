from django.urls import path
from . import views

urlpatterns = [
    path('student/view', views.student),
    path('student/view/<id>', views.student_view),
    path('teacher/view', views.teacher),
    path('teacher/view/<id>', views.teacher_view),
    path('teacher/student/view/<id>', views.teacher_student_view),
    path('view', views.view),
    path('add', views.add),
    path('student/add', views.student_add),
    path('teacher/add', views.teacher_add),
    path('teacher/edit/<id>', views.teacher_edit),
    path('student/edit/<id>', views.student_edit),
    path('student/delete/<int:id>', views.delete_student),
    path('done/<int:id>', views.done),
    path('undone/<int:id>', views.undone),
    path('delete/<id>', views.delete),
    path('model/delete/<id>/<class>', views.model_delete),
]