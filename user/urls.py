from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('complaint/', views.register_complaint, name='complaint'),
    path('track_complaint/', views.track_complaint, name='track_complaint'),
    path('download_complaint/', views.download_complaint, name='download_complaint'),
    path("download_pdf/<int:complaint_id>/", views.download_pdf, name="download_pdf"),
    path('', views.login, name='login'),
]
