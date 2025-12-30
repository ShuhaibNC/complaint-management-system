from django.urls import path
from . import views

urlpatterns = [
    path('manage_users/', views.manage_users, name='update_role'),
    path("update_user_role/<int:user_id>/role/", views.update_user_role, name="update_user_role"),
]
