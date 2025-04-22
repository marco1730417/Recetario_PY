from django.db import models
from autoslug import AutoSlugField

# Create your models here.

class Categorias(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255,null=False)
    slug = AutoSlugField(populate_from='nombre')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'