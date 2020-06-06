from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from classes.models import Class
from classes.models import class_linker
from assignments.models import Assignment
from profiles.models import Profile
import os
import subprocess
from django.contrib import messages

# Create your views here.
def welcome(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, 'welcome.html', {})

def about(request):
    return render(request, 'about.html', {})

def site_map(request):
    return render(request, 'site_map.html', {})

def new(request, *args, **kwargs):
    return render(request, 'typeOfUser.html', {})

def newUser(request, *args, type):
    if request.method == 'POST':
        message = []
        if request.POST.get('password') != request.POST.get('ConformPassword'):
            message.append("The Passwords do not match!")

        try:
            User.objects.get(username = request.POST.get('username'))
        except:
            pass
        else:
            message.append("The username is already Taken!")

        if len(request.POST.get('password')) < 8:
            message.append("The password must be atleast 8 digits!")

        if len(request.POST.get('fullName')) > 30:
            message.append("The Name must be less than 30 digits!")

        if message != []:
            print(args)
            print(request.user)
            return render(request, 'newUser.html', {'message': message})

        user = User()
        user.first_name = request.POST.get('fullName')
        user.username = request.POST.get('username')
        user.set_password(request.POST.get('password'))
        user.save()

        user = authenticate(request, username=user.username, password=request.POST.get('password'))

        login(request, user)

        profile = Profile()
        profile.user_id = request.user.id
        if type == "teacher":
            profile.teacher = True
        profile.save()

        response = redirect('/home')
        return response

    print(args)
    print(request.user)
    return render(request, 'newUser.html', {})

def decidehome(request, *args, **kwargs):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
        if profile.teacher == True:
            response = redirect('/teacher/home')
        elif profile.teacher == False:
            response = redirect('/student/home')
    else:
        response = redirect('/')

    return response

@login_required
def editProfile(request, *args, **kwargs):

    if request.method == 'POST':
        message = []
        if len(request.POST.get('firstname')) > 30:
            message.append("The Name must by less than 30 Digits!")

        if request.user.username != request.POST.get('username'):
            try:
                User.objects.get(username = request.POST.get('username'))
            except:
                pass
            else:
                message.append("The username is already taken!")

        if message != []:
            print(args, kwargs)
            print(request.user)
            return render(request, 'editProfile.html', {'message': message})


        first_name =  request.POST.get('firstname')
        username = request.POST.get('username')
        user = User.objects.get(pk = request.user.id)
        user.first_name = first_name
        user.username = username
        user.save()

        response = redirect('/home')
        return response

    print(args, kwargs)
    print(request.user)
    return render(request, 'editProfile.html', {})

@login_required
def studentHome(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()
    class_link = class_linker.objects.all()
    AssignmentsA = 0
    AssignmentsD = 0
    Classes = 0

    for link in class_link:
        if link.linked_user == request.user:
            Classes += 1

    for assignment in assignments:
        if assignment.user == request.user and assignment.done:
            AssignmentsD += 1
        elif assignment.user == request.user:
            AssignmentsA += 1



    context = {
        'classes': classes,
        'assignments': assignments,
        'AssignmentsA': AssignmentsA,
        'AssignmentsD': AssignmentsD,
        'Classes': Classes
    }

    print(args, kwargs)
    print(request.user)
    return render(request, 'studentHome.html', context)

@login_required
def teacherHome(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()
    AssignmentsA = 0
    AssignmentsD = 0
    Classes = 0

    for classe in classes:
        if classe.teacher == request.user:
            Classes += 1

    context = {
        'classes': classes,
        'assignments': assignments,
        'AssignmentsA': AssignmentsA,
        'AssignmentsD': AssignmentsD,
        'Classes': Classes
    }

    print(args, kwargs)
    print(request.user)
    return render(request, 'teacherHome.html', context)

@login_required()
def logout_request(request):
    logout(request)

    response = redirect("/login")
    return response

@login_required()
def change_password(request):
    user = User.objects.get(pk = request.user.id)

    context = {
        "user": user
    }

    if request.method == "POST":
        if request.POST.get("form_type") == "form-1":
            if user.check_password(request.POST.get('c_pass')):
                return render(request, "change_password_2.html")
            else:
                context["message"] = "Incorrect Password Entered!"
                return render(request, "change_password.html", context)
        elif request.POST.get("form_type") == "form-2":
            pass_1 = request.POST.get("n_pass")
            pass_2 = request.POST.get("n_pass_2")
            message = []

            if request.user.id != 1 and request.user.id != 23:
                if len(pass_1) < 8:
                    message.append("Length of Password must be 8 digits")

            if pass_1 != pass_2:
                message.append("Passwords do not match!")
            if message != []:
                return render(request, "change_password_2.html", {'message': message})

            user = User.objects.get(pk=request.user.id)
            user.set_password(pass_1)
            user.save()
            user = authenticate(request, username=user.username, password=pass_1)
            login(request, user)
            response = redirect("/home")
            return response


    return render(request, "change_password.html", context)

@login_required()
def change_password_2(request, pass_1, pass_2):

    user = User.objects.get(pk=request.user.id)

    if pass_1 == pass_2:
        user.set_password(pass_1)
        user.save()
        user = authenticate(request, username=user.username, password=pass_1)
        login(request, user)
        response = redirect("/home")
        return response

    return render(request, "change_password_2.html", {})


def denied(request, *args, **kwargs):
    return render(request, "denied.html", {})

@login_required
def update(request):

    if not request.user.is_superuser:
        return redirect("/denied")

    message = ""

    if request.method == "POST":
        message = subprocess.run(["git", "pull"], capture_output=True)

    context = {
        'message': message
    }

    return render(request, 'update.html', context)