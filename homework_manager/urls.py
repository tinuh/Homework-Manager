
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('class/', include('classes.urls')),
    path('homework/', include('assignments.urls')),
    path('profile/', include('profiles.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', RedirectView.as_view(url='/home')),
    path('login/', RedirectView.as_view(url='/accounts/login')),
]
