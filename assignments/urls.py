from django.urls import path
from . import views

urlpatterns = [
    path('student/view', views.assignmentsStudent),
    path('student/view/<id>', views.studentAssignmentSpecific),
    path('teacher/view', views.assignmentsTeacher),
    path('teacher/view/<id>', views.teacherAssignmentSpecific),
    path('view', views.view),
    path('add', views.add),
    path('student/add', views.assignmentStudent_add),
    path('teacher/add', views.assignmentTeacher_add),
    path('student/delete/<int:id>', views.deleteStudent),
    path('done/<int:id>', views.done),
    path('undone/<int:id>', views.undone),
    path('delete/<id>', views.delete),
    path('model/delete/<id>/<class>', views.model_delete),
]