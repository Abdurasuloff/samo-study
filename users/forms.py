from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserChangeForm


class CustomUserChangeForm(ModelForm):
      class Meta:
            model=User
            fields = ('first_name', 'last_name', 'username', 'email')