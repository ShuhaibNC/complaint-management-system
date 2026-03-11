from django.shortcuts import render, redirect
import json
from django.http import HttpResponse, JsonResponse
from .models import SOSAlert, Feedback
from user.models import SignupRecord
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
from system_manager.models import Notification

def index(request):
    username = request.session.get("external_username")
    role = None
    if username:
        try:
            user = SignupRecord.objects.get(username=username)
            role = user.role
        except SignupRecord.DoesNotExist:
            role = None
    notification = Notification.objects.all()
    return render(request, 'home/index.html', {'role' : role, 'notification': notification})

def base(request):
    return render(request, 'home/base.html')

def portfolio_adnan(request):
    return render(request, 'home/portfolio_adnan.html')

def portfolio_fadhis(request):
    return render(request, 'home/portfolio_fadhis.html')

def portfolio_sajas(request):
    return render(request, 'home/portfolio_sajas.html')

def portfolio_rahil(request):
    return render(request, 'home/portfolio_rahil.html')

@csrf_exempt
@require_POST
def sos(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        lat = data.get("latitude")
        lng = data.get("longitude")

        # ✅ Validate FIRST before using the values
        if lat is None or lng is None:
            return JsonResponse({"ok": False, "error": "Missing latitude or longitude"}, status=400)

        lat = float(lat)
        lng = float(lng)

        username = request.session.get("external_username")
        geolocator = Nominatim(user_agent="coord_to_district_example")
        location = geolocator.reverse((lat, lng), language="en")
        # ... rest of your code

        if not location:
            return None

        address = location.raw.get("address", {})

        # Different countries use different fields
        district = (
            address.get("state_district")
            or address.get("county")
            or address.get("district")
            or address.get("region")
        )

        if lat is None or lng is None:
            return JsonResponse({"ok": False, "error": "Missing latitude or longitude"}, status=400)

        lat = float(lat)
        lng = float(lng)
    except Exception as e:
        print("ERROR PARSING:", repr(e))
        return JsonResponse({"ok": False, "error": "Invalid data"}, status=400)
    
    email = None

    if username:
        try:
            user = SignupRecord.objects.get(username=username)
            email = user.email
        except SignupRecord.DoesNotExist:
            pass
    alert = SOSAlert.objects.create(
        latitude=lat,
        longitude=lng,
        username=username,
        email=email,
        district=district.lower()
    )

    return JsonResponse({"ok": True, "id": alert.id})

def feedback_view(request):
    if request.method == "POST":
        message = request.POST.get("feedback")

        if not message or not message.strip():
            # If AJAX, return JSON
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": False, "error": "Feedback cannot be empty!"})

            messages.error(request, "Feedback cannot be empty!")
            return redirect("home")

        Feedback.objects.create(message=message)

        # If AJAX, return JSON
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True})

        messages.success(request, "Thank you for your feedback!")
        return redirect("home")

    return redirect("home")

