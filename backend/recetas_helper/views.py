from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404
from http import HTTPStatus
from rest_framework.response import Response 
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date, timedelta
from .models import *
from seguridad.decorators import logueado
from django.contrib.auth.models import User
from recetas.serializers import *
from recetas.models import Recetas
from django.core.files.storage import FileSystemStorage

from django.utils.dateformat import DateFormat
# Create your views here.

class Clase4(APIView):
    
    @logueado()
    def get(self, request,id):     
        try:
            existe=User.objects.filter(pk=id).get()
        except User.DoesNotExist:
            return JsonResponse({"estado":"error","mensaje":"Error al buscar el usuario"},status=HTTPStatus.BAD_REQUEST)
        
        data= Recetas.objects.filter(user_id=id).order_by('-id').all ()
        datos_json=RecetaSerializer(data,many=True)
        return JsonResponse({"estado":"ok","mensaje":"Recetas obtenidas","data":datos_json.data},status=HTTPStatus.OK)


class Clase1(APIView):
    @logueado()
    def post(self, request):
        # Validación de campo 'id'
        receta_id = request.data.get("id")
        if receta_id is None:
            return JsonResponse({"error": "El campo id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        # Buscar la receta
        try:
            receta = Recetas.objects.get(pk=receta_id)
            anterior = receta.foto
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Error al buscar la receta"}, status=HTTPStatus.BAD_REQUEST)

        # Validar si se adjunta imagen
        if 'foto' not in request.FILES:
            return JsonResponse({"estado": "error", "mensaje": "Debe adjuntar una imagen"}, status=HTTPStatus.BAD_REQUEST)

        archivo = request.FILES['foto']
        tipo = archivo.content_type
        if tipo not in ['image/jpeg', 'image/png']:
            return JsonResponse({"estado": "error", "mensaje": "El archivo no es una imagen"}, status=HTTPStatus.BAD_REQUEST)

        # Guardar imagen
        fs = FileSystemStorage()
        try:
            nombre_archivo = f"{datetime.timestamp(datetime.now())}{os.path.splitext(archivo.name)[1]}"
            fs.save(f"recetas/{nombre_archivo}", archivo)
        except Exception:
            return JsonResponse({"estado": "error", "mensaje": "Error al guardar la imagen"}, status=HTTPStatus.BAD_REQUEST)

        # Actualizar receta
        try:
            receta.foto = nombre_archivo
            receta.save()
            if anterior:
                ruta_anterior = f"./uploads/recetas/{anterior}"
                if os.path.exists(ruta_anterior):
                    os.remove(ruta_anterior)
            return JsonResponse({"estado": "ok", "mensaje": "Receta actualizada"}, status=HTTPStatus.OK)
        except Exception:
            return JsonResponse({"estado": "error", "mensaje": "Error al actualizar la receta"}, status=HTTPStatus.BAD_REQUEST)
        
class Clase2(APIView):       
    def get(self, request, slug):
        try:
            data = Recetas.objects.get(slug=slug)
            return JsonResponse({
                "estado": "ok",
                "mensaje": "Receta obtenida",
                "data": {
                    "id": data.id,
                    "slug": data.slug,
                    "tiempo": data.tiempo,
                    "foto": data.foto,
                    "descripcion": data.descripcion,
                    "fecha": DateFormat(data.fecha).format('d/m/Y'),
                    "categoria_id": data.categoria.nombre if data.categoria else None,
                    "imagen": f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}" if data.foto else None,
                    "user_id":data.user_id,
                    "user":data.user.first_name 
                }
            }, status=HTTPStatus.OK)
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Receta no encontrada"}, status=HTTPStatus.NOT_FOUND)


class Clase3(APIView):       
    def get(self, request):
        if(request.GET.get('categoria_id') is None):
            return JsonResponse({"estado": "error", "mensaje": "Error al buscar recetas"}, status=HTTPStatus.BAD_REQUEST)
        try:
            existe=Categorias.objects.filter(pk=request.GET.get('categoria_id')).get()
        except Categorias.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Error al buscar recetas"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            data = Recetas.objects.filter(categoria_id=request.Get.get('categoria_id')).filter(nombre__icontains=request.GET.get('search')).order_by('-id').all()
            datos_json = RecetaSerializer(data, many=True)
            return JsonResponse({"estado": "ok", "mensaje": datos_json.data}, status=HTTPStatus.OK)
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Error al buscar recetas"}, status=HTTPStatus.BAD_REQUEST)
        
class Clase5(APIView):       
    def get(self, request):
        try:
            data = Recetas.objects.order_by('?').all()[:3] # select * from recetes where categori = 6  nombre like '%tortilla%'
            datos_json = RecetaSerializer(data, many=True)
            return JsonResponse({"estado": "ok", "mensaje": datos_json.data}, status=HTTPStatus.OK)
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Error al buscar recetas"}, status=HTTPStatus.BAD_REQUEST)
        