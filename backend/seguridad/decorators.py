from functools import wraps
from jose import jwt
from django.http import HttpResponse, JsonResponse, Http404,HttpResponseRedirect
from django.conf import settings
from http import HTTPStatus
import time
def logueado():
    def metodo(func):
        @wraps(func)
        def _decorator(self, request, *args, **kwargs):  # ← ¡Aquí agregamos `self`!
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return JsonResponse({"error": "No se ha enviado el token"}, status=HTTPStatus.UNAUTHORIZED)

            try:
                tipo, token = auth_header.split(" ")
                if tipo != "Bearer":
                    return JsonResponse({"error": "Tipo de token no válido"}, status=HTTPStatus.UNAUTHORIZED)
            except ValueError:
                return JsonResponse({"error": "Formato de token incorrecto"}, status=HTTPStatus.UNAUTHORIZED)

            try:
                resuelto = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS512"])
            except Exception as e:
                return JsonResponse({"error": "Token no válido"}, status=HTTPStatus.UNAUTHORIZED)

            if int(resuelto["exp"]) > int(time.time()):
                return func(self, request, *args, **kwargs)  # ← Ejecutamos la función original correctamente
            else:
                return JsonResponse({"error": "Token expirado"}, status=HTTPStatus.UNAUTHORIZED)

        return _decorator
    return metodo
