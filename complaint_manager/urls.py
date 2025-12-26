from django.urls import path
from . import views

urlpatterns = [
    path("manage_complaint_cm/", views.manage_complaint_cm, name="manage_complaint_cm"),
    path("document_pdf/<int:complaint_id>/", views.document_pdf, name="document_pdf"),
    path("update_complaint/<int:complaint_id>/", views.update_complaint, name="update_complaint"),
    path("update_status/", views.update_status, name="update_status"),
]