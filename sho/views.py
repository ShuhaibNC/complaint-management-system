from django.shortcuts import render
from home.models import SOSAlert
from user.models import Complaint
from home.models import Feedback

def sos_alerts(request):
    data = SOSAlert.objects.all().order_by('-created_at')
    return render(request, 'sos_alerts.html', {'objects': data})

def manage_complaint(request):
    data = Complaint.objects.all().order_by('-created_at')
    return render(request, 'manage_complaint.html', {'objects': data})

def manage_feedback(request):
    data = Feedback.objects.all().order_by('-created_at')
    return render(request, 'manage_feedback.html', {'objects': data})
