from .views import edit_profile
from django.urls import path


urlpatterns = [
      path('edit-profile', edit_profile, name='update-profile'),
]