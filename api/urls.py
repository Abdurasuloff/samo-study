from django.urls import path, include
from .views import *



urlpatterns = [
     path('bot-users', BotUserCreateView.as_view()),
     path('feedbacks', FeedbackCreateView.as_view()),
     path('courses', CourseListView.as_view()),
     path('attendances', AttendanceListView.as_view()),
     path('payments', AddCashToWalletListView.as_view()),
     path('students', StudentListview.as_view()),

]