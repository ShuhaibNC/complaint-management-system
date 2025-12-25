from django.urls import path
from . import views

urlpatterns = [
    path("manage_complaint_cm/", views.manage_complaint_cm, name="manage_complaint_cm"),
]