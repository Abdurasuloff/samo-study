from django.contrib import admin
from .models import Course, AttendanceGroup,Attendance, Student
# Register your models here.



class AttendanceInline(admin.TabularInline):
      model = Attendance


class AttendanceGroupAdmin(admin.ModelAdmin):
      list_display = ('course',  'time', 'status')
      inlines = [AttendanceInline]


class StudentAdmin(admin.ModelAdmin):
      model = Student
      list_display=( 'id', 'full_name', 'wallet', 'token_id')

admin.site.register(AttendanceGroup, AttendanceGroupAdmin)     
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Student, StudentAdmin)
