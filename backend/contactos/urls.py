from django.urls import path
from .views import *


urlpatterns = [
    path('contactos', Clase1.as_view()),
]
