from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from main.views import Aas
from users.forms import CustomUserChangeForm
# Register your models here.


class UserAdmin(admin.ModelAdmin):
      list_display =( 'first_name', "last_name", 'username', "is_staff", "is_admin", 'is_teacher')
  
      

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)