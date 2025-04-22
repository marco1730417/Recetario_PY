from functools import wraps
from jose import jwt
from django.http import HttpResponse, JsonResponse, Http404,HttpResponseRedirect
from django.conf import settings
from http import HTTPStatus
import time
def logueado():
    def metodo(func):
        @wraps(func)
        def _decorator(request,*args, **kwargs):
            request = args[0]
            if not request.headers.get('Authorization') or request.headers.get('Authorization') == None:
                return JsonResponse({"error":"No se ha enviado el token"},status=HTTPStatus.UNAUTHORIZED)
            header = request.headers.get("Authorization").split(" ")
            
            try:
                resuelto =jwt.decode(header[1], settings.SECRET_KEY, algorithms=["HS512"])
            except Exception as e:
                return JsonResponse({"error":"Token no valido"},status=HTTPStatus.UNAUTHORIZED)    
            
            if int(resuelto["exp"]) > int(time.time()):
                
             return func(*args, **kwargs)
            else:
                return JsonResponse({"error":"Token expirado"},status=HTTPStatus.UNAUTHORIZED)
        return _decorator
    return metodo
