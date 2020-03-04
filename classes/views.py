from django.shortcuts import render
from .models import Class
from .models import class_linker
from assignments.models import Assignment
from assignments.models import Model_assignment
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
import random
from django.contrib.auth.models import User

# Create your views here.
def view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    if profile.teacher == False:
        response = '/class/student/view'
    elif profile.teacher == True:
        response = '/class/teacher/view'
    else:
        response = '/denied'
    return redirect(response)

@login_required
def studentClass(request, *args, **kwargs):
    assignments = Assignment.objects.all()
    class_link = class_linker.objects.all()
    classes = []

    for link in class_link:
        if link.linked_user == request.user:
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
    return render(request, 'studentClass.html', context)
@login_required
def teacherClass(request, *args, **kwargs):

    profile = Profile.objects.get(user = request.user)
    if profile.teacher:
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
        return render(request, "teacherClass.html", context)
    else:
        response = redirect('/denied')
        return response
@login_required
def teacherSpecificClass(request, *args, id):

    profile = Profile.objects.get(user=request.user)
    classe = Class.objects.get(pk=id)
    if profile.teacher and classe.teacher == request.user:

        class_link = class_linker.objects.all()
        model_assignment = Model_assignment.objects.all()
        assignmentss = []
        assignments = Assignment.objects.all()

        count = -1
        for M_assignment in model_assignment:
            if M_assignment.linked_class.id == classe.id:
                count += 1
                assignmentss.append([M_assignment, [0, 0]])
                for assignment in assignments:
                    if assignment.linked_model_assignment.id == M_assignment.id:
                        if assignment.done == True:
                            assignmentss[count][1][0] += 1
                        else:
                            assignmentss[count][1][1] += 1





        context = {
            'assignments': assignmentss,
            'class': classe,
        }

        return render(request, 'teacherClassViewSpecific.html', context)

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

        return render(request, 'studentClassViewSpecific.html', context)

    except:
        response = redirect('/denied')
        return response

@login_required
def class_add(request, *args, **kwargs):

    profile = Profile.objects.get(user = request.user)
    if profile.teacher:

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
    return render(request, 'class_add.html', context)

@login_required
def delete(request, *args, id):
    profile = Profile.objects.get(user = request.user)
    if profile.teacher:
        classes = Class.objects.get(pk = id)
        classes.delete()

        response = redirect('/class/teacher/view')
        return response
    else:
        response = redirect('/denied')
        return response

@login_required
def join_class(request, *args, **kwargs):

    if request.method == "POST":

        classe = Class.objects.get(code = str(request.POST.get('code')))
        class_link = class_linker()
        class_link.linked_user_id = request.user.id
        class_link.enrolled_class_id = classe.id
        class_link.save()

        response = redirect('/class/student/view/' + str(classe.id))
        return response

    print(args, kwargs)
    print(request.user)
    return render(request, "join_class.html", {})

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
    if profile.teacher and exist:
        class_link.delete()

        response = redirect('/class/teacher/view/' + str(class_id))
        return response
    else:
        response = redirect('/denied')
        return response