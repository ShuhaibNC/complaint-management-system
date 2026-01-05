from django.urls import path
from . import views

urlpatterns = [
    path('system_manager/sos_alerts/', views.sm_sos_alerts, name='sm_sos_alerts'),
    path('manage_users/', views.manage_users, name='update_role'),
    path('manage_notification/', views.manage_notification, name='manage_notification'),
    path("manage_notification/", views.manage_notification, name="manage_notification"),
    path(
        "manage_notification/update/<int:pk>/",
        views.update_notification,
        name="update_notification"
    ),
    path("update_user_role/<int:user_id>/role/", views.update_user_role, name="update_user_role"),
    path("manage_complaint_sm/", views.manage_complaint_sm, name="manage_complaint_sm"),
]
