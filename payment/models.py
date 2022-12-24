from django.db import models
from course.models import *
from datetime import date

# Create your models here.
class PayToCourse(models.Model):
      student = models.ForeignKey(Student, on_delete=models.CASCADE)
      course  =  models.ForeignKey(Course, on_delete=models.CASCADE)
      transfer_summ = models.PositiveBigIntegerField()
      date = models.DateField(default = date.today())
      

      def __str__(self):
            return str(self.student.full_name) +  " payed " +str(self.transfer_summ) + " sum to " + str(self.course)


class AddCashToWallet(models.Model):
      student = models.ForeignKey(Student, on_delete = models.CASCADE)
      summ = models.PositiveBigIntegerField()
      date = models.DateField(default = date.today())
      time = models.TimeField(auto_now_add=True, null=True, blank=True,)
      recepient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

      def __str__(self):
            return str(self.summ) + ' is transfered to ' + str(self.student)+ "'s wallet"

class GiveSalary(models.Model):
      teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher")
      salary_summ = models.PositiveBigIntegerField()
      date = models.DateField(default=date.today())
      sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sender")

      def __str__(self):
            return str(self.salary_summ) + ' is given to ' + str(self.teacher)



