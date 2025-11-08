from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, 'home/index.html')
def base(request):
    return render(request, 'home/base.html')
def portfolio(request):
    return render(request, 'home/portfolio.html')
