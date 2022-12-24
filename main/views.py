from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from course.models import *
from datetime import date, timedelta
from django.utils.timezone import now
from payment.models import PayToCourse, AddCashToWallet, GiveSalary
from payment.utils import income_of_teacher_between_dates
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# messages.warning(request, 'Wrong details')
# messages.success(request, 'Wrong details')





"""Bu ustoz o'tadigan darslarni filter qiluvchi funksiya """
def get_courses(request):
      if request.user.is_authenticated:
            teacher = request.user
            courses = Course.objects.filter(teacher=teacher)

            return courses
      else:
            pass      

" Userlarni ularning klanlarigan qarab sahifalarga yuboruvchi index "
@login_required
def index(request):
      if request.user.is_teacher == True:
            return redirect('teacher-dashboard')
      elif request.user.is_admin == True:
            return redirect('reception-dashboard')
      elif request.user.is_staff  == True:
            return redirect('income')   
      else:
            return HttpResponse('Something is wrong with your account')              

"Reception uchun dashboard"
@login_required
def reception_dashboard(request):
      if request.user.is_admin == True or request.user.is_staff == True:
           
            courses= Course.objects.filter(is_ended=False)
            for i in courses:
                 
                  if i.days == "1":
                        i.days = "Dush-Chor-Jum"
                  elif i.days=="2":
                        i.days = "Sesh-Pay-Shan"     
            context = {
                  'students':Student.objects.all(),
                  'courses':courses
            }
            return render(request, 'reception-dashboard.html', context)      
      else:
            messages.warning(request, "Bu sahifaga kirish mumkin emas.")
            return redirect('index')




"""Teacher uchun dasahboard"""
@login_required
def  teacher_dashboard(request):
      teacher = request.user
      courses = Course.objects.filter(teacher=teacher)
      todays_courses = []
      todays_income = 0
      
      start = date.today()-timedelta(days=30)
      end=date.today()
      income_between_dates  = income_of_teacher_between_dates(request, start, end)

      "Bugun bu o'qituvchida qaysi va qachon darsi borligini ko'rsatib turuvchi filter"
      for course in courses:
            weekday = date.today().weekday()
            if int(course.days) == 1 and course.start_date<=date.today():
                  if weekday == 0 or weekday == 2 or weekday == 4:
                        todays_courses.append(course)
            elif int(course.days) == 2 and course.start_date<=date.today():
                  if weekday == 1 or weekday == 3 or weekday == 5:
                        todays_courses.append(course)

      "Bugun  o'qituvchi qancha daromad topganini ko'rsatib turuvchi filter"
      pay_to_courses = PayToCourse.objects.filter(course__in=todays_courses, date=date.today())
      for i in pay_to_courses:
            todays_income += i.transfer_summ/2

      "Ma'lum bir oraliqdagi o'qituvchini qacha daromad qilganini hisoblash uchun forma"
      if request.method =="POST":
            start = request.POST['start']
            end = request.POST['end']
            income_between_dates  = income_of_teacher_between_dates(request, start, end)
      context = {
            'todays_courses':todays_courses,
            "courses":courses,
            'start':str(start),
            'end':str(end),
            'income_between_dates':income_between_dates,
            'todays_income':todays_income,
            'pay_to_courses':pay_to_courses,
            
      }
      return render(request, 'teacher_dashboard.html', context)


"""Har bor kurs yo'qlamasi uchun detail sahifa"""      
@login_required
def attendance_detail(request, id):
      teacher = request.user
      course =  Course.objects.get(id=id, teacher=teacher)
      students_of_course = course.students.all()
      attendance_group = AttendanceGroup.objects.filter(course=course).order_by("date")
      for i in students_of_course:
            for a in attendance_group:
                  abs_students = []
                  abs = Attendance.objects.filter(attendance=a)
                  for b in abs:
                        abs_students.append(b.student)
                  if not i in abs_students:
                        Attendance.objects.create(
                              student=i,
                              present=False,
                              attendance = a,
                              date = a.date

                        )      

            i.attendances = Attendance.objects.filter(student=i, attendance__in=attendance_group).order_by('date')



      context = {
            'course':course,
            'students':students_of_course,
            'attendance_group':attendance_group,
            'courses': get_courses(request) 
            
      }
      return render(request, 'attendance-detail.html', context)

"""Yo'qlamani amalga oshirish"""
def attendance(request, id):
      attendancegroup = AttendanceGroup.objects.get(id=id)
      students = attendancegroup.course.students.all()
      if request.method == "POST":
            for i in students:
                  present = True
                  course_price = attendancegroup.course.price
                  try:  request.POST[str(i.id)]
                  except:
                        present = False
                        course_price = 0 
                 
                  Attendance.objects.create(attendance = attendancegroup, student = i, present = present, date = attendancegroup.date)
                  i.wallet -= course_price
                  i.save()
                  if course_price !=0:
                        PayToCourse.objects.create( 
                        student = i,
                        course = attendancegroup.course,
                        transfer_summ = course_price,
                        )
                 

            total_number_of_students = students.count()
            total_number_of_not_attended_students = Attendance.objects.filter(attendance=attendancegroup, present=False).count()      
            attendancegroup.status = str(total_number_of_not_attended_students) + "  of " + str(total_number_of_students) + " students was not participated in taht lesson"
            attendancegroup.save()
            messages.success(request, 'Davomat olindi.')
            return redirect('course-detail', attendancegroup.course.id  )

      context = {
            'students':students,
            "attendancegroup":attendancegroup,
            'courses': get_courses(request) 
            
      }
      return render(request, 'attendance.html', context)      

"""Har bor kurs  uchun detail sahifa"""      
@login_required
def course_detail(request, id):
      teacher = request.user
      course = Course.objects.get(id=id)
      """Quyidagi kodlar ustozni bugun shu guruhda darsi borligi yoki yo'qligini ko'rsatib turadi."""
      weekday = date.today().weekday()
      have_a_class = False
     
      if int(course.days) == 1 and course.start_date<=date.today():
            if weekday == 0 or weekday == 2 or weekday == 4:
                  have_a_class = True
      elif int(course.days) == 2 and course.start_date<=date.today():
            if weekday == 1 or weekday == 3 or weekday == 5:
                  have_a_class = True
           
            '''attendanceni boshlash'''
      if request.method == "POST":
            if AttendanceGroup.objects.filter(course=course, date=date.today()):
                  attendance_a = AttendanceGroup.objects.get(course=course, date=date.today())
                  messages.warning(request, 'Davomatni o\'zgartitib bo\'lmaydi.')
                  have_a_class= False
                  
            else:      
                  attendance  = AttendanceGroup.objects.create(
                        course=course,
                        time  = course.time,
                        date = date.today(),
                        teacher = teacher,
                        status = 'none'
                  )
                  messages.warning(request, "Ma'lumotlar olinganidan keyin uni o'zgartirib bo'lmaydi.")
                  return redirect('attendance', attendance.id )
      context = {
            'course':course,
            'have_a_class': have_a_class,
            'courses':get_courses(request)
      }
      return render(request, 'course-detail.html', context)

"To'lov qilish"
def make_payment(request):
      if request.method == "POST":
            AddCashToWallet.objects.create(
                  recepient = request.user,
                  summ=int(request.POST['summ']),
                  date = date.today(),
                  student = Student.objects.get(id=request.POST['student_id'])
            )
            messages.success(request, 'To\'lov qabul qilindi.')
            return redirect('reception-dashboard')
      return HttpResponse('To\'lov qilindi')       
      
"O'quvchi qo'shish"
def create_student(request):
      if request.method =="POST":
            Student.objects.create(
                  full_name = request.POST['full_name'],
                  phone_number = request.POST['phone_number']  
            )
            messages.success(request, 'O\'quvchi yaratildi')   
            return redirect('reception-dashboard')  
      return HttpResponse('Yaratildi.')        

"Biror bir studentni kursga qo'shish"

def add_student_to_course(request):
      if request.method =="POST":
            course = Course.objects.get(id = request.POST['course_id'])
            student = Student.objects.get(id=request.POST['student_id'])
            if student in course.students.all():
                  messages.warning(request, "O'quvchi mavjud.")
            else:      
                  course.students.add(student)
                  messages.success(request, "O'quvchi qo'shildi.")
            return redirect('reception-dashboard')
      return HttpResponse('O\'quvchi qo\'shildi')     




"======================================BOSS VIEWS============================================"

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class Aas(UserCreationForm):
      class Meta(UserCreationForm):
            model=User
            fields = ('first_name', 'last_name', 'username', 'email', 'is_staff',  'is_admin', 'is_teacher', 'is_superuser')


class CreateUser(CreateView, LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin):
      form_class = Aas 
      template_name = 'boss/create_user.html'  
      success_url  = '/'
      success_message = "Amal  muvaffaqiyali bajarildi."

      def test_func(self):
            return self.request.user.is_staff == True   

@login_required
def payments(request):
      students = Student.objects.all().order_by('-id')
      if request.user.is_staff == True:
            all_payments = AddCashToWallet.objects.all().order_by('-date')
            if request.method =='POST':
                  start = request.POST['start']
                  end = request.POST['end']
                  if request.POST['student_id']:
                        all_payments = AddCashToWallet.objects.filter(date__gte=start, date__lte=end, student = Student.objects.get(id=request.POST['student_id'])).order_by('date')
                  else :
                        all_payments = AddCashToWallet.objects.filter(date__gte=start, date__lte=end).order_by('date')
            return render(request, 'boss/all_payments.html', {"payments":all_payments, 'students':students})      

      else:
            messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
            return redirect('index') 
                


@login_required
def teachers(request):
      if request.user.is_staff == True:
            teachers = User.objects.filter(is_teacher=True)
            for i in teachers:
                  i.courses = Course.objects.filter(teacher=i)
            
            return render(request, 'boss/all_teachers.html', {"teachers":teachers})      

      else:
            messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
            return redirect('index')     

@login_required
def give_salary(request, teacher_id):
      teacher = User.objects.get(id=teacher_id, is_teacher=True)
      if request.user.is_staff == True and teacher.is_teacher==True:
            
            if request.method =='POST':
                  salary_summ = request.POST['summ']
                  GiveSalary.objects.create(teacher=teacher, salary_summ=salary_summ, sender=request.user)
                  messages.success(request, "Amal bajarildi.")
                  return redirect('teachers')
            return render(request, 'boss/giving_salary.html', {"teacher":teacher})      

      else:
            messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
            return redirect('index')     

@login_required
def students(request):
      if request.user.is_staff == True:
            students = Student.objects.all().order_by('-id')
            for i in students:
                  i.courses = []
                  for a in Course.objects.filter(is_ended=False):
                        if i in a.students.all():
                              i.courses.append(a)
           
            
            return render(request, 'boss/all_students.html', {"students":students})      

      else:
            messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
            return redirect('index')   


@login_required
def salaries(request):
      teachers = User.objects.filter(is_teacher=True)
      if request.user.is_staff == True:
            all_salaries = GiveSalary.objects.all().order_by('-date')
            if request.method =='POST':
                  start = request.POST['start']
                  end = request.POST['end']
                  
                  try:
                        all_salaries = GiveSalary.objects.filter(date__gte=start, date__lte=end, teacher=User.objects.filter(id=request.POST['teacher_id'])).order_by('date')
                  except:
                        all_salaries = GiveSalary.objects.filter(date__gte=start, date__lte=end).order_by('date')
                  
            return render(request, 'boss/all_salaries.html', {"salaries":all_salaries, 'teachers':teachers})      

      else:
            messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
            return redirect('index')     


def courses(request):
      teachers = User.objects.filter(is_teacher=True)
      if request.user.is_staff == True:
            courses = Course.objects.filter(is_ended =False)
            return render(request, 'boss/all_courses.html', {'courses':courses})
      else:
            messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
            return redirect('index')     

class EditCourse(UpdateView, LoginRequiredMixin, SuccessMessageMixin):
      model = Course
      template_name = 'boss/edit_course.html'
      fields = ('name', 'teacher', 'title', 'price', 'students', 'days', 'room', 'end_date', 'is_ended')     
      success_url = '/'
      success_message = "Amal  muvaffaqiyali bajarildi."

class NewCourse(CreateView, LoginRequiredMixin, SuccessMessageMixin):
      model = Course
      template_name = 'boss/create_course.html'
      fields = ('name', 'teacher', 'title', 'price', 'students', 'days', 'room')     
      success_message = "Amal  muvaffaqiyali bajarildi."
      success_url = '/'
             