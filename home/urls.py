from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('portfolio_adnan/', views.portfolio_adnan, name='portfolio_adnan'),
    path('portfolio_fadhis/', views.portfolio_fadhis, name='portfolio_fadhis'),
    path('portfolio_sajas/', views.portfolio_sajas, name='portfolio_sajas'),
    path('portfolio_rahil/', views.portfolio_rahil, name='portfolio_rahil'),
    path("home/sos/", views.sos, name="sos"),
    path("feedback/", views.feedback_view, name="feedback"),

]
