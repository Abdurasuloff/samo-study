from django.db.models.signals import post_save
from django.dispatch import receiver as r
from .models import AddCashToWallet, PayToCourse, GiveSalary

@r(post_save, sender=AddCashToWallet)
def add_cash_to_wallet(sender, instance, created, **kwargs):
      if created:
            instance.student.wallet += instance.summ
            instance.student.save()
 
@r(post_save, sender=PayToCourse)
def transfer_a_half_of_price_of_course_to_teacher(sender, instance, created, **kwargs):
      if created:
            instance.course.teacher.wallet += instance.transfer_summ/2
            instance.course.teacher.save()

@r(post_save, sender=GiveSalary)
def minusing_salary_from_wallet_of_teacher(sender, instance, created, **kwargs):
      if created:
            instance.teacher.wallet -= int(instance.salary_summ)
            instance.teacher.save()

            