from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404
from http import HTTPStatus
from rest_framework.response import Response 
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date, timedelta
from .models import *

from django.utils.text import slugify
from recetas.models import Recetas


# Create your views here.

def  Clase1(request):
    return render(request, 'seguridad/registro.html')