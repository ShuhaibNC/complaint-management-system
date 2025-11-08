from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('complaint/', views.register_complaint, name='complaint'),
]
