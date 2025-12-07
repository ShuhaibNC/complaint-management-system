from django.shortcuts import render
from home.models import SOSAlert

def sos_alerts(request):
    data = SOSAlert.objects.all().order_by('-created_at')
    return render(request, 'sos_alerts.html', {'objects': data})