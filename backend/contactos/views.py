from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404
from http import HTTPStatus
from rest_framework.response import Response 
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date, timedelta
from .models import *
from contactos.models import Contactos
# Create your views here.

#llamamos a utilidades

from utilidades import utilidades

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Clase1(APIView):
     

     @swagger_auto_schema(
        operation_description="Endpoint para Contacto",
        responses={200:"Success",400:"Bad Request"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre':openapi.Schema(type=openapi.TYPE_STRING,description="Nombre"),
                'correo':openapi.Schema(type=openapi.TYPE_STRING,description="Email"),
                'telefono':openapi.Schema(type=openapi.TYPE_STRING,description="telefono"),
                'mensaje':openapi.Schema(type=openapi.TYPE_STRING,description="Mensaje")
                 },
                 required=['nombre','correo','telefono']
                )
            
        )
     
     def post(self, request):
         if(request.data.get('nombre')==None):
             return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
         
         if(request.data.get('correo')==None):
             return JsonResponse({"estado":"error", "mensaje":"El campo correo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
         
         if(request.data.get('telefono')==None):
             return JsonResponse({"estado":"error", "mensaje":"El campo telefono es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
         
         if(request.data.get('mensaje')==None):
             return JsonResponse({"estado":"error", "mensaje":"El campo mensaje es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
         
   
         try:
            Contactos.objects.create(
                nombre=request.data.get('nombre'),
                correo=request.data.get('correo'),
                telefono=request.data.get('telefono'),
                mensaje=request.data.get('mensaje'),
                fecha=datetime.now(),
                )
            
            html =f""" <h1>Hola {request.data.get('nombre')}</h1>
            <p>Gracias por contactarnos, hemos recibido tu mensaje y nos pondremos en contacto contigo a la brevedad.</p>
            <p>Saludos.</p>
                       
            """

            utilidades.sendMail(request.data.get('correo'), "Gracias por contactarnos", html)
            return JsonResponse({"estado":"ok", "mensaje":"Se creo el registro exitosamente"}, status=HTTPStatus.CREATED)
        
         except Exception as e:
            print(f"Error interno: {str(e)}")  # O usar logging
            return JsonResponse({"estado": "error", "mensaje": "Error interno del servidor"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
