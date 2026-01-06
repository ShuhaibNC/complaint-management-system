from django.shortcuts import render, get_object_or_404, redirect
from home.models import SOSAlert
from user.models import SignupRecord
from complaint_manager.models import Complaint as CMComplaint
from home.models import Feedback

def sos_alerts(request):
    username = request.session.get("external_username")
    district = SignupRecord.objects.filter(username=username)\
                                   .values_list("district", flat=True)\
                                   .first()
    data = SOSAlert.objects.filter(district=district).order_by('-created_at')
    return render(request, 'sos_alerts.html', {'objects': data})

def manage_complaint(request):
    username = request.session.get("external_username")

    # get logged user's district
    district = SignupRecord.objects.filter(username=username)\
                                   .values_list("district", flat=True)\
                                   .first()

    # filter complaints by that district
    objects = CMComplaint.objects.filter(district=district,forward=False).order_by('-created_at')

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

def forward_complaint(request, complaint_id):
    complaint = get_object_or_404(CMComplaint, id=complaint_id)

    complaint.forward = True
    complaint.save()

    return redirect("manage_complaint")
