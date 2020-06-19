from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path('login/', TemplateView.as_view(template_name='registration/login.html')),
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('class/', include('classes.urls')),
    path('homework/', include('assignments.urls')),
    path('profile/', include('profiles.urls')),
    path('passwords/', include('passwords.urls')),
    path('accounts/login/', RedirectView.as_view(url='/login')),
    path('accounts/', include('allauth.urls')),
    path('accounts/django/', include('django.contrib.auth.urls')),
    path('accounts/profile/', RedirectView.as_view(url='/home')),
]