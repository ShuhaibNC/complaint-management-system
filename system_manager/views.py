from django.shortcuts import render, get_object_or_404, redirect
from user.models import SignupRecord

def manage_users(request):
    users = SignupRecord.objects.all()
    return render(request, "manage_users.html", {"users": users})

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
