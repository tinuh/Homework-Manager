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
    return render(request, 'landing.html', {})

def about(request):
    return render(request, 'pages/about.html', {})

def site_map(request):
    return render(request, 'pages/site_map.html', {})

def new(request, *args, **kwargs):
    return render(request, 'pages/typeOfUser.html', {})

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
            return render(request, 'register.html', {'message': message})

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
    return render(request, 'register.html', {})

def home(request, *args, **kwargs):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
        if profile.teacher == True:
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
            return render(request, 'pages/teacherHome.html', context)
        elif profile.teacher == False:
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
            return render(request, 'pages/studentHome.html', context)
    else:
        response = redirect('/')

    return response


@login_required()
def logout_request(request):
    logout(request)

    response = redirect("/login")
    return response

def denied(request, *args, **kwargs):
    return render(request, "pages/denied.html", {})

@login_required
def update(request):

    if not request.user.is_superuser:
        return redirect("/denied")

    message = ""

    if request.method == "POST":
        message = subprocess.run(["git", "pull"], stdout=subprocess.PIPE).stdout.decode('utf-8')

    context = {
        'message': message
    }

    return render(request, 'pages/update.html', context)