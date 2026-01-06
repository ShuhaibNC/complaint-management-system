from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import SignupRecord
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from functools import wraps
import datetime
from complaint_manager.models import Complaint
# Create your views here.
from django.http import HttpResponse, Http404, FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        raw_password = request.POST.get("password", "")

        try:
            user = SignupRecord.objects.get(username=username)
        except SignupRecord.DoesNotExist:
            return render(request, "login.html", {"info": "Password or username is incorrect."})
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
        password = request.POST.get("password", "")
        cpassword = request.POST.get("cpassword", "")
        # minimal validation
        if password != cpassword:
            return render(request, "signup.html", {"info": "Password and Confirm Password does not match."})
        if not username or not password or not cpassword:
            return render(request, "signup.html", {"info": "Username and password required."})

        hashed = make_password(password)   # hashes password safely

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
        


        # get district from select
        district = request.POST.get("district", "").strip()

        date_of_incident = None
        if date_str:
            try:
                date_of_incident = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
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
            district=district,
        )

        return render(request, "complaint_register.html", {
            "info": "Complaint registered successfully."
        })

    return render(request, "complaint_register.html")


def track_complaint(request):
    username = request.session.get("external_username")
    cmdata = Complaint.objects.filter(username=username).order_by('-created_at')
    return render(request, 'complaint_tracking.html', {'objects': cmdata})

def download_complaint(request):
    username = request.session.get("external_username")
    objects = Complaint.objects.filter(username=username).order_by('-created_at')
    return render(request, 'download_complaint.html', {'objects': objects})

def download_pdf(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=32,
    )

    styles = getSampleStyleSheet()

    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#111827"),
        spaceAfter=6
    )

    section_title = ParagraphStyle(
        "Section",
        parent=styles["Heading3"],
        fontSize=12,
        textColor=colors.HexColor("#374151"),
        spaceBefore=10,
        spaceAfter=4
    )

    muted = ParagraphStyle(
        "Muted",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#6b7280")
    )

    elements = []

    # Header banner
    banner = Table(
        [["Complaint Report"]],
        colWidths=[470],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1f2937")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 15),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )
    elements.append(banner)
    elements.append(Spacer(1, 10))

    # Metadata
    meta = Table(
        [
            ["Generated On", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
            ["Report ID", f"REP-{complaint.id}"],
        ],
        colWidths=[120, 350],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111827")),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    elements.append(meta)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Complaint Details", heading))
    elements.append(HRFlowable(width="100%", color=colors.HexColor("#d1d5db")))
    elements.append(Spacer(1, 8))

    # Details table
    data = [
        ["Field", "Value"],
        ["Username", complaint.username],
        ["First name", complaint.first_name],
        ["Last name", complaint.last_name],
        ["Email", complaint.email],
        ["Phone", complaint.phone],
        ["District", complaint.district],
        ["Incident date", str(complaint.date_of_incident)],
        ["Created at", str(complaint.created_at)],
    ]

    table = Table(data, colWidths=[140, 330])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [colors.HexColor("#f9fafb"), colors.HexColor("#f3f4f6")]),

        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Description", section_title))
    elements.append(Paragraph(complaint.description or "No description provided.", styles["BodyText"]))
    elements.append(Spacer(1, 18))

    # Footer style
    elements.append(HRFlowable(width="100%", color=colors.HexColor("#e5e7eb")))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("This document was generated automatically.", muted))
    elements.append(Spacer(1, 4))
    if complaint.image:
        elements.append(Spacer(1, 18))
        try:
            img = Image(complaint.image.path, width=260, height=180)
            elements.append(img)
        except Exception:
            pass

    doc.build(elements)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"complaint_report_{complaint.id}.pdf")