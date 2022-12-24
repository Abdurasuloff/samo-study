from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import incomes_in_one_day, incomes_between_two_dates
from datetime import date, timedelta
from django.contrib import messages


# Create your views here.
@login_required 
def income(request):
      user = request.user
      if user.is_staff == True:
            start = date.today()-timedelta(days=30)
            end=date.today()
            incomes_between_dates = incomes_between_two_dates( start, end)
            if request.method == 'POST':
                  start = request.POST['start']
                  end = request.POST['end']
                  incomes_between_dates = incomes_between_two_dates( start, end)
                  
            
            context = {
                  'incomes_between_dates':incomes_between_dates,
                  'todays_income': incomes_in_one_day(date.today()),
                  'start':str(start),
                  'end':str(end),
            }
            return render(request, "income.html", context)
      else:
            messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
            return redirect('index')