from django.shortcuts import render
from home.models import SOSAlert
from user.models import Complaint, SignupRecord
from home.models import Feedback

def sos_alerts(request):
    data = SOSAlert.objects.all().order_by('-created_at')
    return render(request, 'sos_alerts.html', {'objects': data})

def manage_complaint(request):
    username = request.session.get("external_username")

    # get logged user's district
    district = SignupRecord.objects.filter(username=username)\
                                   .values_list("district", flat=True)\
                                   .first()

    # filter complaints by that district
    objects = Complaint.objects.filter(district=district).order_by('-created_at')

    return render(
        request,
        'manage_complaint.html',
        {
            'objects': objects,
            'district': district
        }
    )

def manage_feedback(request):
    data = Feedback.objects.all().order_by('-created_at')
    return render(request, 'manage_feedback.html', {'objects': data})
