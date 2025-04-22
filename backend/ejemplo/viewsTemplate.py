from rest_framework.views import APIView
from django.http import HttpResponse
# Create your views here.

class Class_Ejemplo(APIView):

    def get(self, request):
        return HttpResponse("METODO GET")
    
    def post(self, request):
        return HttpResponse("METODO POST")
      
    
class Class_Ejemplo_Parametros(APIView):

    def get(self, request, id):
        return HttpResponse(f"METODO GET ID: " + str(id))
    
    def put(self, request, id):
       return HttpResponse(f"METODO PUT ID: " + str(id))
    
    def delete(self, request, id):
       return HttpResponse(f"METODO DELETE ID: " + str(id))
    
  
    