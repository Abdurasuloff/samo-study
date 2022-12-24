from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
      is_teacher = models.BooleanField(default=False, help_text = 'Agar yaratilayotgan foydalanuvchi ustoz bo\'lsa.')
      is_admin  = models.BooleanField(default = False,  help_text = 'Agar yaratilayotgan foydalanuvchi adminstrator bo\'lsa.')
      wallet = models.PositiveBigIntegerField(default=0)
      user = Us er
      def __str__(self):
            if  self.is_teacher == True and self.is_admin ==False:
                  return  "Teacher " + str( self.first_name ) + " "+str(self.last_name)
            elif self.is_teacher == False and self.is_admin ==True:      
                  return  "Admin "+ str( self.first_name ) + " "+str(self.last_name)
            else:
                  return str( self.first_name ) + " "+str(self.last_name)

