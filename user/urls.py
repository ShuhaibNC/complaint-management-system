from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('complaint/', views.register_complaint, name='complaint'),
    path('track_complaint/', views.track_complaint, name='track_complaint'),
    path('', views.login, name='login'),
]
