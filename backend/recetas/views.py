from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404
from http import HTTPStatus
from rest_framework.response import Response 
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date, timedelta
from .models import *
from .serializers import *
from django.utils.text import slugify
from django.utils.dateformat import DateFormat
from dotenv import load_dotenv
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage

# Create your views here.
class Clase1(APIView):
     
     def post(self, request):
    # Validaciones de campos obligatorios
        campos_obligatorios = ['nombre', 'tiempo', 'descripcion', 'categoria_id']
        for campo in campos_obligatorios:
            if not request.data.get(campo):
                return JsonResponse({"estado": "error", "mensaje": f"El campo {campo} es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

    # Validar existencia de la categoría
            if not Categorias.objects.filter(pk=request.data.get('categoria_id')).exists():
                return JsonResponse({"estado": "error", "mensaje": "La categoría no se encuentra disponible"}, status=HTTPStatus.BAD_REQUEST)

    # Validar nombre de la receta
        if Recetas.objects.filter(nombre=request.data.get('nombre')).exists():
            return JsonResponse(
            {"estado": "error", "mensaje": f"El nombre de la receta {request.data.get('nombre')} ya se encuentra en uso"},
            status=HTTPStatus.BAD_REQUEST
        )

    # Manejo de archivo (foto)
        archivo = request.FILES.get('foto')
        if not archivo:
                return JsonResponse({"estado": "error", "mensaje": "Debe adjuntar una foto para la receta"}, status=HTTPStatus.BAD_REQUEST)

        if archivo.content_type not in ['image/jpeg', 'image/png']:
            return JsonResponse({"estado": "error", "mensaje": "El archivo no es una imagen válida"}, status=HTTPStatus.BAD_REQUEST)

        try:
        # Obtener extensión y generar nombre único
            extension = os.path.splitext(archivo.name)[1]
            fecha = datetime.now()
            foto_nombre = f"{datetime.timestamp(fecha)}{extension}"

            # Guardar archivo
            fs = FileSystemStorage()
            filename = fs.save(f"recetas/{foto_nombre}", archivo)
            file_url = fs.url(filename)  # Obtener la URL del archivo

        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Se produjo un error al intentar subir el archivo"}, status=HTTPStatus.BAD_REQUEST)

    # Crear la receta en la base de datos
        try:
            Recetas.objects.create(
            nombre=request.data.get('nombre'),
            tiempo=request.data.get('tiempo'),
            descripcion=request.data.get('descripcion'),
            categoria_id=request.data.get('categoria_id'),
            fecha=fecha,
            foto=foto_nombre  # Guarda el nombre del archivo
        )
            return JsonResponse({"estado": "ok", "mensaje": "Se creó el registro exitosamente"}, status=HTTPStatus.CREATED)

        except Exception as e:
            raise Http404
     
     def get(self, request):
         data = Recetas.objects.order_by('-id').all()
         datos_json= RecetaSerializer(data, many=True)
         # return Response({"estado":"ok", "mensaje":datos_json.data}, status=HTTPStatus.OK)
         return JsonResponse({"estado":"ok", "data":datos_json.data}, status=HTTPStatus.OK)
    
class Clase2(APIView):
    
    def get(self, request, id):
        try:
            data = Recetas.objects.get(id=id)
            datos_json= RecetaSerializer(data)
            return JsonResponse({"data":{"id":data.id, "nombre":data.nombre, "slug":data.slug,"tiempo":data.tiempo,"foto":data.foto,"descripcion":data.descripcion,"fecha":DateFormat(data.fecha).format('d/m/Y'),"categoria":data.categoria.nombre,"categoria_id":data.categoria_id ,"imagen":f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}" }, "estado":"ok"}, status=HTTPStatus.OK)
            #return JsonResponse({"estado":"ok", "data":datos_json.data}, status=HTTPStatus.OK)
        except Recetas.DoesNotExist:
            raise Http404
        
    def put(self, request, id):
        
        try:
            data = Recetas.objects.filter(pk=id).get()
        except Recetas.DoesNotExist:
            raise Http404
     
      # Validaciones de campos obligatorios
        campos_obligatorios = ['nombre', 'tiempo', 'descripcion', 'categoria_id']
        for campo in campos_obligatorios:
            if not request.data.get(campo):
                return JsonResponse({"estado": "error", "mensaje": f"El campo {campo} es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
    # Validar existencia de la categoría
            if not Categorias.objects.filter(pk=request.data.get('categoria_id')).exists():
                return JsonResponse({"estado": "error", "mensaje": "La categoría no se encuentra disponible"}, status=HTTPStatus.BAD_REQUEST)

     
        try:  
            data = Recetas.objects.filter(pk=id).get()
            Recetas.objects.filter(pk=id).update(
                nombre=request.data.get('nombre'),
                slug=slugify(request.data.get('nombre')),
                descripcion=request.data.get('descripcion'),
                tiempo=request.data.get('tiempo'),
                categoria_id=request.data.get('categoria_id'))
                
            #return JsonResponse({"data":{"id":data.id, "nombre":data.nombre, "slug":data.slug}}, status=HTTPStatus.OK)
            return JsonResponse({"estado":"ok", "mensaje":"Se actualizo el registro exitosamente"}, status=HTTPStatus.OK)
        except Recetas.DoesNotExist:
            raise Http404
        
        
    def delete(self, request, id):
        try:
            data =Recetas.objects.filter(pk=id).get() 
        except Recetas.DoesNotExist:
            raise Http404
        
        #borrar la foto de la carpeta
        os.remove(f"./uploads/recetas/{data.foto}")
        
        #borrar el registro de la bd
        Recetas.objects.filter(pk=id).delete()
        return JsonResponse({"estado":"ok", "mensaje":"Se elimino el registro exitosamente"}, status=HTTPStatus.OK)