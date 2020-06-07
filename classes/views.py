from django.shortcuts import render
from .models import Class
from .models import class_linker
from assignments.models import Assignment
from assignments.models import Model_assignment
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
import random
from django.contrib.auth.models import User

# Create your views here.

@login_required
def view(request):
    if request.user.profile.teacher:
        response = '/class/teacher/view'
    else:
        response = '/class/student/view'
    return redirect(response)

@login_required
def studentClass(request, *args, **kwargs):
    assignments = Assignment.objects.all()
    class_link = class_linker.objects.filter(linked_user_id = request.user.id)
    classes = []

    for link in class_link:
        classe = Class.objects.get(pk = link.enrolled_class.id)
        classes.append(classe)

    context = {
        'classes': classes,
        'assignments': assignments,
        'class_link': class_link,
        'class_linker': class_linker
    }

    print(args, kwargs)
    print(request.user)
    return render(request, 'classes/student/index.html', context)

@login_required
def teacherClass(request, *args, **kwargs):
    if request.user.profile.teacher:
        assignments = Assignment.objects.all()
        class_link = class_linker.objects.all()
        classes = Class.objects.all()
        classee = []

        for classe in classes:
            if classe.teacher == request.user:
                classee.append(classe)

        classes = classee

        context = {
            'classes': classes,
            'assignments': assignments,
            'class_link': class_link,
            'class_linker': class_linker
        }

        print(args, kwargs)
        print(request.user)
        return render(request, "classes/teacher/index.html", context)
    else:
        response = redirect('/denied')
        return response

@login_required
def teacherSpecificClass(request, *args, id):
    try:
        classe = Class.objects.get(pk=id)
    except:
        return redirect("/denied")
    if request.user.profile.teacher and classe.teacher == request.user:
        class_link = class_linker.objects.filter(enrolled_class_id=classe.id)
        model_assignment = Model_assignment.objects.all()
        assignmentss = []
        assignments = Assignment.objects.filter()
        profiles = Profile.objects.all()
        students = []


        for links in class_link:
            students.append(links.linked_user)

        count = -1
        assignmentsC = 0
        for M_assignment in model_assignment:
            if M_assignment.linked_class.id == classe.id:
                count += 1
                assignmentsC += 1
                assignmentss.append([M_assignment, [0, 0]])
                assignments = Assignment.objects.filter(linked_model_assignment_id = M_assignment.id)
                for assignment in assignments:
                    if assignment.done == True:
                        assignmentss[count][1][0] += 1
                    else:
                        assignmentss[count][1][1] += 1

        context = {
            'assignments': assignmentss,
            'assignmentsC': assignmentsC,
            'class': classe,
            'students': students,
            'studentsA': len(students),
        }

        return render(request, 'classes/teacher/view.html', context)

    else:
        response = redirect('/denied')
        return response

@login_required
def studentSpecificClass(request, *args, id):

    try:
        classe = Class.objects.get(pk=id)

        class_link = class_linker.objects.get(linked_user = request.user, enrolled_class = classe)
        assignments = Assignment.objects.all()
        assignmentsA = 0
        assignmentss = []

        for assignment in assignments:
            if assignment.user == request.user and assignment.linked_class == classe:
                assignmentss.append(assignment)
                assignmentsA += 1

        assignments = assignmentss

        context = {
            'class': classe,
            'assignments': assignments,
            'assignmentsA': assignmentsA,
        }

        return render(request, 'classes/student/view.html', context)

    except:
        response = redirect('/denied')
        return response

@login_required
def class_add(request, *args, **kwargs):

    if request.user.profile.teacher:

        classes = Class.objects.all()
        assignments = Assignment.objects.all()

        context = {
            'classes': classes,
            'assignments': assignments,
        }

        if request.method == "POST":
            classes = Class()
            classes.name = request.POST.get('name')
            classes.description = request.POST.get('description')
            classes.teacher_id = request.user.id
            choice = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
            while True:
                code = ""
                for i in range(6):
                    code += random.choice(choice)
                try:
                    Class.objects.get(code = code)
                except:
                    break
            classes.code = code
            classes.save()

            classe = Class.objects.get(code = code)

            response = '/class/teacher/view/' + str(classe.id)
            response = redirect(response)
            return response
    else:
        response = redirect('/denied')
        return response
    print(args, kwargs)
    print(request.user)
    return render(request, 'classes/teacher/add.html', context)

@login_required
def class_edit(request, *args, **kwargs):
    id = kwargs['id']

    go = False
    try:
        classe = Class.objects.get(pk = id)
        if classe.teacher.id == request.user.id:
            go = True
    except:
        go = False
    if request.user.profile.teacher and go:

        context = {
            'class': classe,
        }

        if request.method == "POST":
            classe = Class.objects.get(pk = id)
            classe.name = request.POST.get('name')
            classe.description = request.POST.get('description')
            classe.teacher_id = request.user.id
            classe.save()

            classe = Class.objects.get(pk = id)

            response = '/class/teacher/view/' + str(classe.id)
            response = redirect(response)
            return response
    else:
        response = redirect('/denied')
        return response
    print(args, kwargs)
    print(request.user)
    return render(request, 'classes/teacher/edit.html', context)

@login_required
def delete(request, *args, id):
    try:
        classes = Class.objects.get(pk=id)
    except:
        return redirect('/denied')

    if request.user.profile.teacher and classes.teacher_id == request.user.id:
        classes.delete()

        response = redirect('/class/teacher/view')
        return response
    else:
        response = redirect('/denied')
        return response

@login_required
def join_class(request, *args, **kwargs):
    if request.method == "POST":
        try:
            classe = Class.objects.get(code = str(request.POST.get('code')))
        except:
            context = {
                'message': "The class code is invalid!"
            }

            return render(request, "classes/student/join.html", context)

        try:
            before = class_linker.objects.get(enrolled_class_id=classe.id, linked_user_id=request.user.id)
        except:
            pass
        else:
            context = {
                'message': "You cannot join a class twice!"
            }

            return render(request, "classes/student/join.html", context)

        class_link = class_linker()
        class_link.linked_user_id = request.user.id
        class_link.enrolled_class_id = classe.id
        class_link.save()

        model_assiginments = Model_assignment.objects.filter(linked_class_id = classe.id)

        for assignment in model_assiginments:
            new_assign = Assignment()
            new_assign.linked_class_id = classe.id
            new_assign.name = assignment.name
            new_assign.description = assignment.description
            new_assign.linked_class_linker_id = class_link.id
            new_assign.linked_model_assignment_id = assignment.id
            new_assign.user_id = request.user.id
            new_assign.save()

        response = redirect('/class/student/view/' + str(classe.id))
        return response

    print(args, kwargs)
    print(request.user)
    return render(request, "classes/student/join.html", {})

@login_required
def remove_student(request,*args, class_id, user_id):

    profile = Profile.objects.get(user=request.user)
    exist = True
    try:
        classe = Class.objects.get(pk = class_id)
        user = User.objects.get(pk = user_id)
        class_link = class_linker.objects.get(enrolled_class=classe,linked_user=user)
    except:
        exist = False
    if (profile.teacher or request.user.id == user_id) and exist:
        class_link.delete()

        if profile.teacher:
            response = redirect('/class/teacher/view/' + str(class_id))
        else:
            response = redirect('/class/student/view')
        return response
    else:
        response = redirect('/denied')
        return response