from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404,HttpResponseRedirect
from http import HTTPStatus
from rest_framework.response import Response 
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date, timedelta
from .models import UsersMetadata

from django.utils.text import slugify
from .models import *

from django.contrib.auth.models import User
from dotenv import load_dotenv
import os
import uuid 

from utilidades import utilidades



# Create your views here.

class Clase1(APIView):
    def post(self, request):
        if request.data.get('nombre')==None or request.data.get("nombre")==None :
            return JsonResponse({"error":"El campo nombre es obligatorio"},status=HTTPStatus.BAD_REQUEST)
        
        if request.data.get('correo')==None or request.data.get("correo")==None :
            return JsonResponse({"error":"El campo correo es obligatorio"},status=HTTPStatus.BAD_REQUEST)        
        
        
        if request.data.get('password')==None or request.data.get("password")==None :
            return JsonResponse({"error":"El campo password es obligatorio"},status=HTTPStatus.BAD_REQUEST)        
        
        
        if User.objects.filter(email=request.data.get('correo')).exists():
            return JsonResponse({"error":"El correo ya se encuentra registrado"},status=HTTPStatus.BAD_REQUEST)        

        token = uuid.uuid4()
        url=f"{os.getenv("BASE_URL")}api/v1/seguridad/verificacion/{token}"
        
        try:
            u=User.objects.create_user(
                email=request.data.get('correo'),
                username=request.data.get('correo'),
                password=request.data.get('password'),
                first_name=request.data.get('nombre'),
                last_name="",
                is_active=0
            )
           # Insercion en cascada
            
            UsersMetadata.objects.create(
                user_id=u.id,
                token=token,
            )
            
            html=f"""<h3>Hola {request.data.get('nombre')}</h3> 
            <p>Para activar tu cuenta, haz click en el siguiente enlace:</p>
            <a href="{url}">Activar cuenta</a>
            """
            utilidades.sendMail(request.data.get('correo'), "Activar cuenta", html)
        except Exception as e:
            return JsonResponse({"error":"Error al crear el usuario"},status=HTTPStatus.BAD_REQUEST)
        
        return JsonResponse({"message":"Usuario creado correctamente"},status=HTTPStatus.CREATED)
    
    
class Clase2(APIView):
        
        def get(self, request, token):
            if token==None or not token:
                return JsonResponse({"error":"El token es obligatorio"},status=HTTPStatus.BAD_REQUEST)
            try:
                data=UsersMetadata.objects.filter(token=token).get()
                
                UsersMetadata.objects.filter(token=token).update(token="")
                User.objects.filter(id=data.user_id).update(is_active=1)
                
                return HttpResponseRedirect(os.getenv("BASE_URL_FRONTEND"))
                
            except UsersMetadata.DoesNotExist:
                raise Http404("Token no válido")
          