from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UsersMetadata(models.Model):
    token = models.CharField(max_length=50,blank=True,null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
  
    def __str__(self):
       return f"{self.first_username} {self.last_name}"
  
    class Meta:
      db_table = 'users_metadata'
      verbose_name = 'UserMetadata'
      verbose_name_plural = 'User Metadata'