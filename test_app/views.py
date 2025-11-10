from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse

def hello_user(request: HttpRequest, user_name):
    return HttpResponse(f"<h1>Hello, {user_name}!<h1>")
