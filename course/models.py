from random import choices
from django.db import models
from users.models import User
from datetime import date
import random

# Create your models here.
times = (
        ('1', '7.30:9.30'),
        ('2', '10.00:12:00'),
        ('3', '13.00:15.00'),
        ('4', '15.30:17.30'),
    )
days = (
      ('1', 'Dush-Chor-Jum'),
      ('2', 'Sesh-Pay-Shan')
)    



class Student(models.Model):
      full_name = models.CharField(max_length=200)
      phone_number = models.CharField(max_length=120)
      wallet = models.IntegerField(default=0)
      token_id = models.CharField(default=str(random.randint(10000000, 99999999)), max_length=150)

      def __str__(self):
            return str(self.full_name)



class Course(models.Model):
      name  = models.CharField(max_length=120)
      teacher = models.ForeignKey(User, on_delete = models.CASCADE)
      title = models.TextField(null=True, blank=True)
      price = models.PositiveBigIntegerField()
      students = models.ManyToManyField(Student)
      time = models.CharField(max_length = 150 , choices=times)
      days = models.CharField(max_length = 150 , choices=days)
      room =  models.PositiveBigIntegerField()
      start_date = models.DateField(default=date.today())
      end_date = models.DateField(null=True, blank=True)
      is_ended = models.BooleanField(default=False)
  

      def __str__(self):
            return str(self.name) + " " + str(self.days) +" "+ str(self.time) +"in"+str(self.room)


class AttendanceGroup(models.Model):
      course = models.ForeignKey(Course, on_delete=models.CASCADE)
      time = models.CharField(max_length = 150 , choices=times)
      date = models.DateField()
      teacher = models.ForeignKey(User, on_delete = models.CASCADE)
      status = models.CharField(max_length=150)

      def __str__(self):
            return str(self.status)


class Attendance(models.Model):
      attendance = models.ForeignKey(AttendanceGroup, on_delete=models.CASCADE)
      student = models.ForeignKey(Student, on_delete=models.CASCADE)
      date = models.DateField(default = date.today())
      present = models.BooleanField(default=True)
      

      def __str__(self):
            return str(self.student)+" "+str(self.present)






