from django.shortcuts import render, get_object_or_404, redirect
from user.models import SignupRecord
from user.models import Complaint
from home.models import SOSAlert
from .models import Notification

def sm_sos_alerts(request):
    data = SOSAlert.objects.order_by('-created_at')
    return render(request, 'sos_alerts.html', {'objects': data})

def manage_complaint_sm(request):
    data = Complaint.objects.order_by('-created_at')
    return render(request, 'sm_manage_complaint.html', {'objects': data})

def manage_users(request):
    users = SignupRecord.objects.all()
    return render(request, "manage_users.html", {"users": users})

def manage_notification(request):
    notification, created = Notification.objects.get_or_create(
        singleton_enforcer=True,
        defaults={
            "title": "Default Title",
            "message": "Write your notification here",
            "status": "inactive",
        },
    )

    return render(request, "manage_notification.html", {
        "notification": notification
    })

def update_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)

    if request.method == "POST":
        notification.title = request.POST.get("title", notification.title)
        notification.message = request.POST.get("message", notification.message)
        notification.status = request.POST.get("status", notification.status)

        notification.save()
        return render(request, "manage_notification.html", {
        "notification": notification, "info": "Notification updated successfully."
    })

    # If somehow accessed via GET, just return to the page
    return redirect("manage_notification")

def update_user_role(request, user_id):
    user = get_object_or_404(SignupRecord, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role", "").strip()
        new_district = request.POST.get("district", "").strip()

        updated = False

        if new_role:
            user.role = new_role
            updated = True

        if new_district:
            user.district = new_district
            updated = True

        if updated:
            user.save()

    return redirect("update_role")
