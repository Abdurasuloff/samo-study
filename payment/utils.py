from .models import AddCashToWallet, PayToCourse, Course




def incomes_in_one_day(date):
      total_income = 0
      expected_income = 0
      
      payments =  AddCashToWallet.objects.filter(date = date) 
      pay_to_courses = PayToCourse.objects.filter(date=date)
      
      for i in payments:
            total_income += i.summ

      for i in pay_to_courses:
            expected_income += i.transfer_summ      


      context = {
            'total_income':total_income,
            'expected_income':expected_income,
            'wage_of_teachers': expected_income/2,
            'payments':payments,
            'pay_to_courses':pay_to_courses,
      }   
      return context      

def incomes_between_two_dates(start, end):
      total_income = 0
      expected_income = 0
      payments = AddCashToWallet.objects.filter(date__gte=start, date__lte=end).order_by('date')
      pay_to_courses = PayToCourse.objects.filter(date__gte=start, date__lte=end).order_by('date')
      for i in payments:
            total_income += i.summ
      for i in pay_to_courses:
            expected_income += i.transfer_summ     
      context = {
            'total_income':total_income,
            'expected_income':expected_income,
            'wage_of_teachers': expected_income/2,
            'payments':payments,
            'pay_to_courses':pay_to_courses, 
      } 
 
      return context   


def income_of_teacher_between_dates(request, start, end):
      teacher = request.user
      income = 0
      courses = Course.objects.filter(teacher=teacher)
      pay_to_courses = PayToCourse.objects.filter(course__in=courses, date__gte=start, date__lte=end).order_by('date')
      for i in pay_to_courses:
            income += i.transfer_summ   

      return {'income':income, 'pay_to_courses':pay_to_courses}