from django.shortcuts import render
from .serializers import *
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from course.models import Attendance
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.serializers import serialize as serik
# Create your views here.


class CourseListView(ListAPIView):
      queryset = Course.objects.all()
      serializer_class = CourseSerializer

class BotUserCreateView(ListCreateAPIView):
      queryset = BotUsers.objects.all()
      serializer_class = BotUserSerializer

class FeedbackCreateView(CreateAPIView):
      queryset = Feedback.objects.all()
      serializer_class = FeedbackSerializer      

class AttendanceListView(ListAPIView):
      queryset = Attendance.objects.all()
      serializer_class = AttendanceSerializer      

class AddCashToWalletListView(ListAPIView):
      queryset = AddCashToWallet.objects.all()
      serializer_class = AddCashToWalletSerializer      

class StudentListview(ListAPIView):
      queryset = Student.objects.all()
      serializer_class = StudentSerializer      



"""def show_payments(request, token):
      
      student = Student.objects.get(token_id=token)
      payments = AddCashToWallet.objects.filter(student=student)
      payments_json = serializers.serialize('json', payments)
      return HttpResponse(payments_json, content_type='application/json')
"""
