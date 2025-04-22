from django.db import models

# Create your models here.

# Create your models here.

class Contactos(models.Model):
    nombre = models.CharField(max_length=255,null=True, blank=True)
    correo = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255,null=True, blank=True)
    mensaje = models.TextField(null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'contactos'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'