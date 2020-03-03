from django.shortcuts import render
from classes.models import Class
from classes.models import class_linker
from .models import Assignment
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from .models import Model_assignment

# Create your views here.
@login_required
def view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    if profile.teacher == False:
        response = '/homework/student/view'
    elif profile.teacher == True:
        response = '/homework/teacher/view'
    else:
        response = '/denied'
    return redirect(response)

@login_required
def add(request):
    profile = Profile.objects.get(user_id = request.user.id)
    if profile.teacher == False:
        response = '/homework/student/add'
    elif profile.teacher == True:
        response = '/homework/teacher/add'
    else:
        response = '/denied'
    return redirect(response)

@login_required()
def assignmentsTeacher(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()
    model_assignments = Model_assignment.objects.all()
    assignmentNames = []
    count = -1

    for model_assignment in model_assignments:
        if model_assignment.linked_teacher == request.user:
            count += 1
            assignmentNames.append([model_assignment, [0, 0]])
            for assignment in assignments:
                if assignment.linked_model_assignment == model_assignment:
                    if assignment.done == True:
                        assignmentNames[count][1][0] += 1
                    else:
                        assignmentNames[count][1][1] += 1

    assignmentCount = len(assignmentNames)

    context = {
        'classes': classes,
        'assignmentNames': assignmentNames,
        'assignmentCount': assignmentCount,
    }

    print(args, kwargs)
    print(request.user)
    return render(request, 'teacherAssignment.html', context)


@login_required
def assignmentsStudent(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()
    AssignmentsA = 0
    AssignmentsD = 0

    for assignment in assignments:
        if assignment.user == request.user and assignment.done == False:
            AssignmentsA += 1

    for assignment in assignments:
        if assignment.user == request.user and assignment.done == True:
            AssignmentsD += 1


    context = {
        'classes': classes,
        'assignments': assignments,
        'AssignmentsA': AssignmentsA,
        'AssignmentsD': AssignmentsD,
    }

    print(args, kwargs)
    print(request.user)
    return render(request, 'studentAssignment.html', context)

@login_required
def assignmentStudent_add(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()

    context = {
        'classes': classes,
        'assignments': assignments,
    }

    if request.method == "POST":
        assignments = Assignment()
        assignments.name = request.POST.get('name')
        assignments.description = request.POST.get('description')
        assignments.user_id = request.user.id
        assignments.save()

        response = redirect('/homework/view')
        return response
    print(args, kwargs)
    print(request.user)
    return render(request, 'studentAssignment_add.html', context)

@login_required
def assignmentTeacher_add(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()
    classess = []

    for classe in classes:
        if classe.teacher_id == request.user.id:
            classess.append(classe)

    classes = classess
    context = {
        'classes': classes,
        'assignments': assignments,
    }

    if request.method == "POST":
        class_link = class_linker.objects.all()
        model_assiginments = Model_assignment.objects.all()

        model_assiginment = Model_assignment(name = request.POST.get('name'),description = request.POST.get('description') ,linked_teacher_id = request.user.id, linked_class_id = request.POST.get('class'))
        model_assiginment.save()

        for student in class_link:
            if str(student.enrolled_class.id) == str(request.POST.get('class')):
                assignments = Assignment(name = request.POST.get('name'), description = request.POST.get('description'), linked_class_id = request.POST.get('class'), user_id = student.linked_user.id, linked_model_assignment_id = int(model_assiginment.id))
                assignments.save()

        class_object = Class.objects.get(id = int(str(request.POST.get('class')))).id
        response = redirect('/class/teacher/view/' + str(class_object))
        return response
    print(args, kwargs)
    print(request.user)
    return render(request, 'teacherAssignment_add.html', context)

@login_required
def deleteStudent(request, *args, id):

    assignment = Assignment.objects.get(pk = id)
    assignment.delete()

    response = redirect("/homework/view")
    return response

@login_required
def done(request, *args, id):

    assignment = Assignment.objects.get(pk = id)
    assignment.done = True
    assignment.save()

    response = redirect("/homework/view")
    return response

@login_required
def undone(request, *args, id):

    assignment = Assignment.objects.get(pk = id)
    assignment.done = False
    assignment.save()

    response = redirect("/homework/view")
    return response