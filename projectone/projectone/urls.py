 
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from django.conf.urls.static import static
from django.conf import settings

from Users.api import views

def index(request):
    return HttpResponse("Welcome to the Django API")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('Users.api.urls')),
     path('', index),  # Define a root URL handler
    path('upload/', views.upload_view, name='upload'),  # Include the upload URL
    path('upload_success/', views.upload_success, name='upload_success'),  # Inclu
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)