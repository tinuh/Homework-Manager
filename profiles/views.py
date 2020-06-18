from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

@login_required
def edit(request, *args, **kwargs):

    if request.method == 'POST':
        message = []
        if len(request.POST.get('firstname')) > 30:
            message.append("The First Name must by less than 30 Digits!")
        if len(request.POST.get('lastname')) > 30:
            message.append("The Last Name must by less than 30 Digits!")

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
            return render(request, 'profiles/edit.html', {'message': message})


        first_name =  request.POST.get('firstname')
        last_name =  request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = User.objects.get(pk = request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()

        response = redirect('/home')
        return response

    print(args, kwargs)
    print(request.user)
    return render(request, 'profiles/edit.html', {})

@login_required
def change_password(request):
    user = User.objects.get(pk = request.user.id)

    context = {
        "user": user
    }

    if request.method == "POST":
        if request.POST.get("form_type") == "form-1":
            if user.check_password(request.POST.get('c_pass')):
                return render(request, "profiles/change_password_2.html")
            else:
                context["message"] = "Incorrect Password Entered!"
                return render(request, "profiles/change_password.html", context)
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
                return render(request, "profiles/change_password_2.html", {'message': message})

            user = User.objects.get(pk=request.user.id)
            user.set_password(pass_1)
            user.save()
            user = authenticate(request, username=user.username, password=pass_1)
            login(request, user)
            response = redirect("/home")
            return response

    if request.user.has_usable_password():
        return render(request, "profiles/change_password.html", context)
    else:
        return render(request, "profiles/change_password_2.html", context)

def add(request, *args, **kwargs):
    id = request.user.id

    try:
        Profile.objects.get(user_id=id)
    except:
        profile = Profile()
        profile.user_id = id
        profile.save()
        return redirect("/set/type")
    
    return redirect("/home")