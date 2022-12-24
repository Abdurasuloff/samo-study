from course.models import Course, Attendance, Student
from rest_framework import serializers
from .models import *
from payment.models import AddCashToWallet




class CourseSerializer(serializers.ModelSerializer):
      class Meta:
            model = Course
            fields = "__all__"
            depth = 1

class BotUserSerializer(serializers.ModelSerializer):
      class Meta:
            model  = BotUsers
            fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
      class Meta:
            model  = Feedback
            fields = "__all__"   

class AttendanceSerializer(serializers.ModelSerializer):
      class Meta:
            model = Attendance
            fields = "__all__"
            depth = 2

class AddCashToWalletSerializer(serializers.ModelSerializer):
      class Meta:
            model = AddCashToWallet
            fields = "__all__"
            depth = 2

class StudentSerializer(serializers.ModelSerializer):
     
      class Meta:
            model = Student
            fields = "__all__"
            depth = 2
