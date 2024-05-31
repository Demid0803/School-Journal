from django.shortcuts import render
import hashlib
from datetime import datetime, timedelta
from .models import PseudoUser, Token
from rest_framework.decorators import api_view
from rest_framework.response import Response



# Create your views here.

@api_view(["GET" , "POST"])
def token_create(request):
    data = request.data
    if request.method == "POST":
        if "email" not in data or "password" not in data:
            return Response({"status" : "error" , "message":"Передайте ключ email и password"})
        if Token.objects.filter(email=data["email"]).exists():
            return Response({"status" : "error" , "message":"Токен уже существует"})
        user_obj = PseudoUser.objects.filter(email=data["email"])
        if not user_obj.exists():
            return Response({"status" : "error" , "message":"Такого пользователя нет!"})
        if user_obj[0].password_hash != hashlib.sha256(data["password"].encode()).hexdigest():
            return Response({"status" : "error" , "message":"Пароль не совпадает!"})
        date_now = datetime.now()
        token = f'{data["email"]}.{user_obj[0].password_hash}.{date_now}'
        token = hashlib.sha512(token.encode()).hexdigest()
        date = date_now + timedelta(days=7)
        Token.objects.create(email=data["email"], date_expired=date, token=token)
        return Response({"status" : "succsess", "token": token})
    return Response({"message":"Здесь вы можете получить токен на срок 7 дней"})



@api_view(["GET" , "POST"])
def token_refresh(request):
    data = request.data
    if request.method == "POST":
        if "email" not in data or "password" not in data:
            return Response({"status" : "error" , "message":"Передайте ключ email и password"})
        if not Token.objects.filter(email=data["email"]).exists():
            return Response({"status" : "error" , "message":"Токен не существует"})
        user_obj = PseudoUser.objects.filter(email=data["email"])
        if not user_obj.exists():
            return Response({"status" : "error" , "message":"Такого пользователя нет!"})
        if user_obj[0].password_hash != hashlib.sha256(data["password"].encode()).hexdigest():
            return Response({"status" : "error" , "message":"Пароль не совпадает!"})
        date_now = datetime.now()
        token = f'{data["email"]}.{user_obj[0].password_hash}.{date_now}'
        token = hashlib.sha512(token.encode()).hexdigest()
        date = date_now + timedelta(days=7)
        Token.objects.filter(email=data["email"]).update(date_expired=date, token=token)
        return Response({"status" : "succsess", "token": token})
    return Response({"message":"Здесь вы можете получить токен на срок"})




