from django.shortcuts import render
from user.models import Complaint

def manage_complaint_cm(request):
    data = Complaint.objects.all().order_by('-created_at')
    return render(request, 'cm_manage_complaint.html', {'objects': data})