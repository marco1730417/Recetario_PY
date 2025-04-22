from django.db import models
from autoslug import AutoSlugField
from categorias.models import Categorias

# Create your models here.

class Recetas(models.Model):
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING)
    nombre = models.CharField(max_length=255,null=False)
    slug = AutoSlugField(populate_from='nombre',max_length=100)
    tiempo = models.CharField(max_length=100,null=True)
    foto = models.CharField(max_length=100,null=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'recetas'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'