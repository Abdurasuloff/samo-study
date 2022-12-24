from django.urls import path
from .views import *

urlpatterns = [
      path('', index, name='index'),
      path('reception-dashboard', reception_dashboard, name='reception-dashboard'),
      path('teacher-dashboard', teacher_dashboard, name='teacher-dashboard'),
      path('attendance-detail/<int:id>', attendance_detail, name='attendance-detail'),
      path('course-detail/<int:id>', course_detail, name='course-detail'),
      path('attendance/<int:id>', attendance, name='attendance'),
      #Post viewlar
      path('make-payment', make_payment, name='make-payment'),
      path('create-student', create_student, name='create-student'),
      path('add-student-to-course', add_student_to_course, name='add-student-to-course'),
      #Boss views
      path('staff/create-user', CreateUser.as_view(), name='create-user'),
      path('staff/payments', payments, name='payments'),
      path('staff/teachers', teachers, name='teachers'),
      path('staff/students', students, name='students'),
      path('staff/salaries', salaries, name='salaries'),
      path('staff/give-salary/<int:teacher_id>', give_salary, name='give-salary'),
      path('staff/courses', courses, name='courses'),
      path('staff/edit-course/<int:pk>', EditCourse.as_view(), name='edit-course'),
      path('staff/new-course', NewCourse.as_view(), name='create-course'),

]