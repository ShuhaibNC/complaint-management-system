from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path("home/sos/", views.sos, name="sos"),
    path("feedback/", views.feedback_view, name="feedback"),

]
