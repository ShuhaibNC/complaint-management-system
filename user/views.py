from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def signup(request):
    return render(request, 'register/signup.html')

def register_complaint(request):
    return render(request, 'register/complaint_register.html')