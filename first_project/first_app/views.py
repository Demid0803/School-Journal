from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Teacher, Student, Class, Days_Balls, StudentToClass, Subject, TeacherByClass, Balls
from re import match
from custom_auth.models import Token, PseudoUser
from datetime import datetime, timezone

@api_view(["GET", "POST"])
def start(request):
    if request.method == "POST":
        def __str__():
            return Response({"message":"Это дневник, проект не до конца доработан, попробуйте что-то ввести"})




@api_view(["GET", "POST"])
def get_all_teachers(request):
    if request.method == "POST":
        if  "token" not in request.data:
            return Response({"status": "error", "message": "Пожалуйста, передайте токен "})
        user = get_user(request.data["token"])
        if user["status"] == "error":
            return Response(user)
        result = {
            "teachers" : []
        }
        for teacher in Teacher.objects.all():
            result["teachers"].append([teacher.id, teacher.name, teacher.class_id.id, teacher.subject])
        return Response(result)
    return Response({"message" : "Здесь вы можете получить информацию про всех учителей"})


@api_view(["GET", "POST"])
def get_all_classes(request):
    if request.method == "POST":
        if "token" not in request.data:
            return Response({"status": "error", "message": "Пожалуйста, передайте токен "})
        user = get_user(request.data["token"])
        if user["status"] == "error":
            return Response(user)
        result = {
            "classes": []
        }
        for classe in Class.objects.all():
            result["classes"].append([classe.id, classe.name, classe.top])
        return Response(result)
    return Response({"message" : "Здесь вы можете получить информацию про все классы"})

@api_view(["GET", "POST"]) # Возьмем класс ... заложников?
def get_class(request):
    if request.method == "POST":
        data = request.data
        if  "token" not in data:
            return Response({"status": "error", "message": "Пожалуйста, передайте токен "})
        user = get_user(request.data["token"])
        if user["status"] == "error":
            return Response(user)
        if user["user"]["role"] == "Teacher":
            result = {
                    "classes" : []
                }
            query = TeacherByClass.objects.filter(teacher_id=user["user"]["role_id"])
            for pair in query:
                print("Цикл идет(бежит, в школу опаздывает)")
                result["classes"].append({
                    "name": pair.class_id.name,
                    "subject": pair.subject_id.name,
                    "students": []
                })
                for student_obj in StudentToClass.objects.filter(class_id=pair.class_id):
                    result["classes"][-1]["students"].append(student_obj.student_id.name)
            return Response(result)

        elif user["role"] == "Student":
            result = {
                    "homeroom" : None,
                    "student" : []
                }
            class_obj = StudentToClass.objects.filter(student_id=user["role_id"])[0].class_id
            for student_obj in StudentToClass.objects.filter(class_id=class_obj):
                result["students"].append(student_obj.name)
            return Response(result)
        else:
            return Response({"status": "error", "message": "У вас нет доступа к этой функции, потому что Вы user, а я Admin(ха-ха)"})    
    return Response({"message" : "Здесь вы можете получить информацию про любой класс"})


@api_view(["GET", "POST"])
def add_balls(request): # Прикрутить винтики...это...ФИКСИКИ
    if request.method == 'POST':
        data = request.data
        if "token" not in data:
            return Response({"status": "error", "message": "Передайте пожалуйста токен"})
        user = get_user(data["token"])
        if user["status"] == "error":
            return Response(user)
        if user["user"]["role"] != "Teacher":
            return Response({"status": "error", "message": "Forbidden"})
        
        if not ("student_id" in data.keys() and "subject_id" in data.keys() and "balls" in data.keys()):
            return Response({"status": "error", "message": "Нужно передать три ключа: student_id, subject, balls(А у Вас есть 3 квартиры или Вы работаете завхозом?)"})
        if not (isinstance(data["student_id"], int) and isinstance(data["subject_id"], int) and isinstance(data["balls"], str)):
            return Response({"status": "error", "message": "student_id и subject_id должны быть числом, а balls - строкой"})
        if match(r'^\d$', data["balls"]) is None:
            return Response({"status": "error", "message": "Передайте одну оценку в формате строки"})
        student_obj = Student.objects.filter(id=data['student_id'])
        teacher_obj = Teacher.objects.filter(id=user["user"]["role_id"])
        subject_obj = Subject.objects.filter(id=data["subject_id"])
        if not (student_obj.exists() and teacher_obj.exists() and subject_obj.exists()):
            return Response({"status": "error", "message": "Студента | Учителя | Предмета не существует(они в школу не пришли)"})
        stc_obj = StudentToClass.objects.filter(student_id=student_obj[0])
        tbc_obj = TeacherByClass.objects.filter(teacher_id=teacher_obj[0], subject_id=subject_obj[0])
        if not (stc_obj.exists() and tbc_obj.exists()):
            return Response({"status": "error", "message": "Не существуют, и всё тут!"})
        if stc_obj[0].class_id != tbc_obj[0].class_id:
            return Response({"status": "error", "message": "Вы не можете ставить оценку этому ученику"})
        daysballs_obj = Days_Balls.objects.filter(student_id=student_obj[0], subject_id=subject_obj[0])
        if daysballs_obj.exists():
            daysballs_obj.update(balles=daysballs_obj[0].balles+data['balls'])
        else:
            Days_Balls.objects.create(student_id=student_obj, subject_id=subject_obj, balles=data["balls"])
        return Response({"status": "success"})
    return Response({'message': 'Здесь вы можете добавить оценки'})

# Chipi-chipi-chapa-chapa-dubi-dubi-daba-daba------magic-BOOOM-BOOM-BOOM-BOOM
@api_view(["GET", "POST"])
def remove_balls(request): # У разрабов здесь конь не валялся
    if request.method == 'POST':
        data = request.data
        if "token" not in data:
            return Response({"status": "error", "message": "Передайте пожалуйста токен"})
        user = get_user(data["token"])
        if user["status"] == "error":
            return Response(user)
        if user["user"]["role"] != "Teacher":
            return Response({"status": "error", "message": "Forbidden"})
        if not ("student_id" in data.keys() and "subject_id" in data.keys()):
            return Response({"status": "error", "message": "Нужно передать два ключа: student_id, subject"})
        if not (isinstance(data["student_id"], int) and isinstance(data["subject_id"], int)):
            return Response({"status": "error", "message": "student_id и subject_id должны быть числом"})
        student_obj = Student.objects.filter(id=data['student_id'])
        teacher_obj = Teacher.objects.filter(id=user["user"]["role_id"])
        subject_obj = Subject.objects.filter(id=data["subject_id"])
        if not (student_obj.exists() and teacher_obj.exists() and subject_obj.exists()):
            return Response({"status": "error", "message": "Студента | Учителя | Предмета не существует"})
        stc_obj = StudentToClass.objects.filter(student_id=student_obj[0])
        tbc_obj = TeacherByClass.objects.filter(teacher_id=teacher_obj[0], subject_id=subject_obj[0])
        if not (stc_obj.exists() and tbc_obj.exists()):
            return Response({"status": "error", "message": "Не существуют"})
        if stc_obj[0].class_id != tbc_obj[0].class_id:
            return Response({"status": "error", "message": "Вы не можете ставить оценку этому ученику"})
        daysballs_obj = Days_Balls.objects.filter(student_id=student_obj[0], subject_id=subject_obj[0])
        if daysballs_obj.exists() and len(daysballs_obj[0].balles) > 0:
            daysballs_obj.update(balles=daysballs_obj[0].balles[0:-1]) 
        else:
            return Response({"status": "error", "message": "ЛЮДИ!!! Поставьте хотя бы ОДНУ - ОДНУ оценку чтобы её УДАЛИТЬ!!!"})
        return Response({"status": "success"})
    return Response({'message': 'Здесь вы можете убрать оценки'})


def get_user(token):
    token_obj = Token.objects.filter(token=token)
    if not token_obj.exists():
        return {"status" : "error", "message":"Токен не существует, создайте его"}
    if token_obj[0].date_expired < datetime.now(timezone.utc):
        return {"status" : "error", "message":"Токен просрочен"}
    user_obj = PseudoUser.objects.filter(email=token_obj[0].email)[0]
    return {"status" : "success", "user": {
        "email" : user_obj.email,
        "role" : user_obj.role,
        "role_id" : user_obj.role_id
    }}


@api_view(["GET", "POST"])
def get_quater_balls(request): # У разрабов здесь конь не валялся
    if request.method == 'POST':
        data = request.data
        if "token" not in data:
            return Response({"status": "error", "message": "Передайте пожалуйста токен"})
        user = get_user(data["token"])
        if user["status"] == "error":
            return Response(user)
        if user["user"]["role"] != "Teacher":
            return Response({"status": "error", "message": "Forbidden"})
        
        if not ("class_id" in data.keys() and "subject_id" in data.keys()):
            return Response({"status": "error", "message": "Нужно передать два ключа class_id, subject(ипотеку оплатили на 2 квартиры?)"})
        if not (isinstance(data["student_id"], int) and isinstance(data["subject_id"], int)):
            return Response({"status": "error", "message": "class_id и subject_id должны быть числом(ЦИФРОЙ!!!!!)"})
        class_obj = Class.objects.filter(id=data['class_id'])
        subject_obj = Subject.objects.filter(id=data["subject_id"])
        teacher_obj = Teacher.objects.filter(id=user["user"]["role_id"])
        if not (class_obj.exists() and teacher_obj.exists() and subject_obj.exists()):
            return Response({"status": "error", "message": "Класса | Учителя | Предмета не существует, дак говорю, в школу не пришли"})
        stc_obj = StudentToClass.objects.filter(class_id=class_obj[0])
        for student_obj in stc_obj:
            days_balls_obj = Days_Balls.objects.filter(student_id=student_obj, subject_id=subject_obj)
            balls = list(map(int, list(days_balls_obj[0].balles)))
            arg = round(sum(balls)/len(balls))
            days_balls_obj.update(balls=" ")
            # Нужно будет сделать словарь result, в котором будет храниться итоговая оценка по каждому ученику
            # 1) Нужно сделать start
            # 2) Протестить add_balls, remove_balls
            # 3) Доделать функцию get_quarter_balls
            result = {
                "students" : []
            }
            for bal, stud  in Balls.objects.all(), Student.objects.all():
                result["students"].append([stud.name, bal.s1, bal.s2, bal.s3, bal.s4, bal.all_year])
        return Response(result)
    return Response({'message': 'Здесь вы можете вывести оценки за четверти и за год(*видит их только учитель*)'})
