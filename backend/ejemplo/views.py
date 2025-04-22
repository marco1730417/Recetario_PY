from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404
from http import HTTPStatus
from rest_framework.response import Response  
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date, timedelta
import os
# Create your views here.

class Class_Ejemplo(APIView):

   # def get(self, request):
    #    return HttpResponse(f"METODO GET | id={request.GET.get('id')} | slug = {request.GET.get('slug')}")
    
    def get(self, request):
      #Retornos con JSON
 #     return JsonResponse({"estado":"ok", "mensaje":f"METODO GET | id={request.GET.get('id', None)} | slug = {request.GET.get('slug')}"})

      return JsonResponse({"estado":"ok", "mensaje":f"METODO GET | id={request.GET.get('id', None)} | slug = {request.GET.get('slug')}"}, status=HTTPStatus.OK)

    def post(self, request):
        if request.data.get('correo')==None or request.data.get("password")==None :
            raise Http404
        
        return JsonResponse({"estado":"ok", "mensaje":f"METODO POST | correo={request.data.get('correo', None)} | password = {request.data.get('password')}"}, status=HTTPStatus.CREATED)

    
class Class_Ejemplo_Parametros(APIView):

    def get(self, request, id):
        return HttpResponse(f"METODO GET ID: " + str(id))
    
    def put(self, request, id):
       return HttpResponse(f"METODO PUT ID: " + str(id))
    
    def delete(self, request, id):
       return HttpResponse(f"METODO DELETE ID: " + str(id))
    
class Class_Ejemplo_Upload(APIView):
  
  def post(self, request):
        try:
            # Validar si se envió un archivo
            if 'file' not in request.FILES:
                return JsonResponse({"estado": "error", "mensaje": "No se envió ningún archivo"}, status=400)
            
            archivo = request.FILES['file']
            extension = os.path.splitext(archivo.name)[1]  # Obtiene la extensión del archivo
            
            # Validar extensión del archivo (Opcional)
            extensiones_permitidas = [".jpg", ".png", ".pdf", ".docx"]
            if extension.lower() not in extensiones_permitidas:
                return JsonResponse({"estado": "error", "mensaje": "Formato de archivo no permitido"}, status=400)

            fs = FileSystemStorage()
            fecha = datetime.now()
            nombre_archivo = f"{datetime.timestamp(fecha)}{extension}"
            
            # Guardar archivo
            filename = fs.save(f"ejemplo/{nombre_archivo}", archivo)
            file_url = fs.url(filename)  # Obtener la URL del archivo

            return JsonResponse({"estado": "ok", "mensaje": "Se subió correctamente", "url": file_url})

        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": str(e)}, status=400)
    