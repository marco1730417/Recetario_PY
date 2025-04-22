from django.urls import path
from .views import Class_Ejemplo, Class_Ejemplo_Parametros, Class_Ejemplo_Upload


urlpatterns = [
    path('ejemplo', Class_Ejemplo.as_view()),

    path('ejemplo/<int:id>', Class_Ejemplo_Parametros.as_view()),
    
    path('ejemplo-upload', Class_Ejemplo_Upload.as_view()),
]
