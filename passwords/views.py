from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import ResetPWD
import smtplib
from homework_manager.env import env
from django.contrib.auth import login, authenticate
from django.utils import timezone
from datetime import timedelta, time

# Create your views here.
@login_required
def add(request):
    if not request.user.is_superuser:
        return redirect("/denied")

    if request.method == "POST":
        new_request = ResetPWD()
        new_request.user_id = request.POST.get("user")
        new_request.email = request.POST.get("email")
        new_request.save()

        reset_request = ResetPWD.objects.get(id = new_request.id)

        #start SMTP server
        server = smtplib.SMTP(env("SMTP_SERVER"), env("SMTP_PORT"))
        server.ehlo()
        server.starttls()
        server.login(env("EMAIL"), env("EMAIL_PWD"))

        #send email
        msg = "Dear Homework Manager User, \n\n" \
              "     A New password reset request has been placed for the user: " + reset_request.user.username + ". Reset it at the link https://homework.tinu.tech/passwords/reset/" + reset_request.code + " \n \n Thank you for using the Homework Manager."

        server.sendmail(env("EMAIL"), reset_request.email, "\r\n".join(
            ["From: " + env("EMAIL"), "To: " + reset_request.email, "Subject: Password Reset Request (Homework Manager)", "", msg]))

        #Stop the SMTP Server
        server.quit()
        
        return redirect("/passwords/add")

    users = User.objects.all()

    context = {
        'users': users,
    }

    return render(request, "passwords/add.html", context)

def reset(request, **kwargs):

    code = kwargs["code"]

    try:
        pwd_object = ResetPWD.objects.get(code = code)
    except:
        return redirect("/denied")

    if request.method == "POST":
        pass_1 = request.POST.get("n_pass")
        pass_2 = request.POST.get("n_pass_2")
        message = []

        if len(pass_1) < 8:
            message.append("Length of Password must be 8 digits")

        if pass_1 != pass_2:
            message.append("Passwords do not match!")
        if message != []:
            return render(request, "profiles/change_password_2.html", {'message': message})

        user = User.objects.get(pk=pwd_object.user.id)
        user.set_password(pass_1)
        user.save()
        user = authenticate(request, username=user.username, password=pass_1)
        login(request, user)
        response = redirect("/home")
        pwd_object.delete()
        return response


    return render(request, "profiles/change_password_2.html", {})

