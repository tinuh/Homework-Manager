from django.shortcuts import HttpResponseRedirect

def login_required(function):
    def wrapper(request, *args, **kw):
        user=request.user
        if not (user.id and request.session.get('code_success')):
            return HttpResponseRedirect('/login/')
        else:
            return function(request, *args, **kw)
    return wrapper