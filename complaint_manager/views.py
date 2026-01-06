from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse, JsonResponse
import datetime
from complaint_manager.models import Complaint
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Complaint
from user.models import SignupRecord


def manage_complaint_cm(request):
    username = request.session.get("external_username")
    district = SignupRecord.objects.filter(username=username)\
                                   .values_list("district", flat=True)\
                                   .first()
    data = Complaint.objects.filter(district=district, forward=True).order_by('-created_at')
    return render(request, 'cm_manage_complaint.html', {'objects': data})

def document_pdf(request, complaint_id):
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

def update_complaint(request, complaint_id):
    objects = Complaint.objects.filter(id=complaint_id)
    return render(request, 'update_complaint.html', {'objects': objects})

@require_POST
@csrf_exempt   # optional if CSRF causes trouble during testing
def update_status(request):
    try:
        data = json.loads(request.body)
        complaint_id = data.get("id")
        status_text = data.get("status")

        if not complaint_id or not status_text:
            return JsonResponse({"success": False, "error": "Missing parameters"})

        obj = Complaint.objects.get(id=complaint_id)
        obj.status = status_text
        obj.save()

        return JsonResponse({"success": True})

    except Complaint.DoesNotExist:
        return JsonResponse({"success": False, "error": "Complaint not found"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})