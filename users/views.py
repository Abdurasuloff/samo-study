from django.shortcuts import render, redirect
from .models import User
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def edit_profile(request):
      form = CustomUserChangeForm(request.POST)
      if request.method =="POST":
         if form.is_valid():
            user = User.objects.get(username=request.user.username)
            obj = form.cleaned_data
            user.first_name = obj['first_name']
            user.last_name = obj['last_name']
            user.username = obj['username']
            user.email = obj['email']
            user.save()
            messages.success(request, "Amal bajarildi.")
            return redirect('index')
      return render(request, 'registration/edit-profile.html', {'form': form, 'user':request.user})      
