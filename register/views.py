from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def register(request):
    return render(request, 'register/register.html')
