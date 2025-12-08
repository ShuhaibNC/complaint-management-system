from django.urls import path
from . import views

urlpatterns = [
    path('home/sos_alerts/', views.sos_alerts, name='sos_alerts'),
    path("manage_complaint/", views.manage_complaint, name="manage_complaint"),
    path("manage_feedback/", views.manage_feedback, name="manage_feedback"),
]
