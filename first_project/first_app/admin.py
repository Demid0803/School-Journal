from django.contrib import admin
from .models import Student, Class, StudentToClass, Teacher, Balls, Days_Balls, TeacherByClass, Subject
# Register your models here.

admin.site.register(Student)
admin.site.register(Class)
admin.site.register(StudentToClass)
admin.site.register(Teacher)
admin.site.register(Balls)
admin.site.register(Days_Balls)
admin.site.register(TeacherByClass)
admin.site.register(Subject)