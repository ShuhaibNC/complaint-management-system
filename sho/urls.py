from django.urls import path
from . import views

urlpatterns = [
    path('home/sos_alerts/', views.sos_alerts, name='sos_alerts'),
]
