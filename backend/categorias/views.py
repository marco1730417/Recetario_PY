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
from recetas.models import Recetas
# Create your views here.
class Clase1(APIView):
     
     def post(self, request):
         if(request.data.get('nombre')==None):
             return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
         try:
            Categorias.objects.create(
                nombre=request.data.get('nombre'))

            return JsonResponse({"estado":"ok", "mensaje":"Se creo el registro exitosamente"}, status=HTTPStatus.CREATED)
         except Exception as e:
            raise Http404
     
     def get(self, request):
         data = Categorias.objects.order_by('-id').all()
         datos_json= CategoriaSerializer(data, many=True)
         # return Response({"estado":"ok", "mensaje":datos_json.data}, status=HTTPStatus.OK)
         return JsonResponse({"estado":"ok", "data":datos_json.data}, status=HTTPStatus.OK)
    
class Clase2(APIView):
    
    def get(self, request, id):
        try:
            data = Categorias.objects.get(id=id)
            datos_json= CategoriaSerializer(data)
            return JsonResponse({"data":{"id":data.id, "nombre":data.nombre, "slug":data.slug}}, status=HTTPStatus.OK)
            #return JsonResponse({"estado":"ok", "data":datos_json.data}, status=HTTPStatus.OK)
        except Categorias.DoesNotExist:
            raise Http404
        
    def put(self, request, id):
        if(request.data.get('nombre')==None):
             return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get('nombre'):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:  
            data = Categorias.objects.filter(pk=id).get()
            Categorias.objects.filter(pk=id).update(
                nombre=request.data.get('nombre'),
                slug=slugify(request.data.get('nombre'))
                
            )
            #return JsonResponse({"data":{"id":data.id, "nombre":data.nombre, "slug":data.slug}}, status=HTTPStatus.OK)
            return JsonResponse({"estado":"ok", "mensaje":"Se actualizo el registro exitosamente"}, status=HTTPStatus.OK)
        except Categorias.DoesNotExist:
            raise Http404
        
        
    def delete(self, request, id):
        try:
            data =Categorias.objects.filter(pk=id).get() 
        except Categorias.DoesNotExist:
            raise Http404
        
        if Recetas.objects.filter(categoria=id).exists():
            return JsonResponse({"estado":"error", "mensaje":"No se puede eliminar la categoria porque tiene recetas asociadas"}, status=HTTPStatus.BAD_REQUEST)    
        Categorias.objects.filter(pk=id).delete()
        return JsonResponse({"estado":"ok", "mensaje":"Se elimino el registro exitosamente"}, status=HTTPStatus.OK)