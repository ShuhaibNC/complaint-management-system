from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import SignupRecord
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from functools import wraps
from datetime import datetime
from .models import Complaint
# Create your views here.
from django.http import HttpResponse

def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        raw_password = request.POST.get("password", "")

        try:
            user = SignupRecord.objects.get(username=username)
        except SignupRecord.DoesNotExist:
            return render(request, "login/login.html", {"info": "Password or username is incorrect."})
        if check_password(raw_password, user.password_hash):
            request.session['external_user_id'] = user.id
            request.session['external_username'] = user.username
            return redirect("home")
        else:
            return render(request, "login.html", {"info": "Password or username is incorrect."})

    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        raw_password = request.POST.get("password", "")

        # minimal validation
        if not username or not raw_password:
            return render(request, "signup.html", {"info": "Username and password required."})

        hashed = make_password(raw_password)   # hashes password safely

        SignupRecord.objects.create(
            username=username,
            email=email,
            password_hash=hashed
        )

        return render(request, "signup.html", {"info": "Signup Success."})
    return render(request, "signup.html")

@csrf_protect
def register_complaint(request):
    if request.method == "POST":
        username = request.session.get("external_username")
        fname = request.POST.get("fname", "").strip()
        lname = request.POST.get("lname", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        description = request.POST.get("description", "").strip()
        date_str = request.POST.get("date", "")
        image_file = request.FILES.get("image")

        date_of_incident = None
        if date_str:
            try:
                date_of_incident = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                date_of_incident = None

        if not fname or not lname or not email or not description:
            return render(request, "complaint_register.html", {
                "info": "Please fill all required fields."
            })

        Complaint.objects.create(
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            phone=phone,
            description=description,
            date_of_incident=date_of_incident,
            image=image_file,
        )

        return render(request, "complaint_register.html", {"info": "Complaint registered successfully."})

    return render(request, "complaint_register.html")

def track_complaint(request):
    data = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaint_tracking.html', {'objects': data})