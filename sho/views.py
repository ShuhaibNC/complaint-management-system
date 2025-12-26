from django.shortcuts import render, get_object_or_404, redirect
from home.models import SOSAlert
from user.models import Complaint, SignupRecord
from complaint_manager.models import Complaint as CMComplaint
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

def forward_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)


    CMComplaint.objects.create(
        username=complaint.username,
        first_name=complaint.first_name,
        last_name=complaint.last_name,
        email=complaint.email,
        phone=complaint.phone,
        district=complaint.district,
        description=complaint.description,
        date_of_incident=complaint.date_of_incident,
        image=complaint.image
    )

    return redirect("manage_complaint")
