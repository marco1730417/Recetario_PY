from django.shortcuts import render,HttpResponse

# Create your views here.

def home_inicio(request):
    return HttpResponse("hola mundo")