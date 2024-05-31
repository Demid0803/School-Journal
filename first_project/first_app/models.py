from django.db import models

# Create your models here.

# Student - ID, ФИО, рейтинг(?)
# Класс - ID, имя, рейтинг класса
# StudentToClass - ID Класса, ID ученика
# Учителя - ID, ФИО, ID класса, предмет
# Оценки - ID ученика, предмет, 1ч, 2ч, 3ч, 4ч, годовая оценка
# (ПОТОМ) Ежедневные оценки - ID ученика, предмет, оценки, средний балл


class Student(models.Model):
    name = models.CharField(max_length=100)
    top = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Class(models.Model):
    name = models.CharField(max_length=3)
    top = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class StudentToClass(models.Model):
    class_id = models.ForeignKey("first_app.Class", on_delete=models.CASCADE)
    student_id = models.ForeignKey("first_app.Student", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Класс: {self.class_id.name}, ФИО студента:{self.student_id.name}"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    class_id = models.ForeignKey("first_app.Class", on_delete=models.CASCADE)

    def __str__(self):
        return f"Учитель ФИО: {self.name}, ID класса: {self.class_id}"
class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Balls(models.Model):
    student_id = models.ForeignKey("first_app.Student", on_delete=models.CASCADE)
    subject_id = models.ForeignKey("first_app.Subject", on_delete=models.DO_NOTHING)
    s1 =  models.PositiveIntegerField()
    s2 =  models.PositiveIntegerField()
    s3 =  models.PositiveIntegerField()
    s4 =  models.PositiveIntegerField()
    all_year = models.PositiveIntegerField()
class Days_Balls(models.Model):
    student_id = models.ForeignKey("first_app.Student", on_delete=models.CASCADE)
    subject_id = models.ForeignKey("first_app.Subject", on_delete=models.DO_NOTHING)
    balles = models.CharField(max_length=100)

class TeacherByClass(models.Model):
    teacher_id = models.ForeignKey("first_app.Teacher", on_delete=models.CASCADE)
    class_id = models.ForeignKey("first_app.Class", on_delete=models.CASCADE)
    subject_id = models.ForeignKey("first_app.Subject", on_delete=models.CASCADE)


