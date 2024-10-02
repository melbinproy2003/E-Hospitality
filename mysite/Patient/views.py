from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.utils import timezone
from guest.models import PatientTable
from Webadmin.models import DoctorTable, DepartmentTable, AssignDoctor
from .models import AppoinmentTable, MedicalHistory, payment
from Doctor.models import Prescribition
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def patient_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.session.get('type') != 'patient':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper_func

@patient_required
def profile(request):
    id = request.session.get('id')
    profile = PatientTable.objects.get(id=id)
    return render(request, 'patient/profile.html', {'profile': profile, 'id': id})

@patient_required
def update_patient_profile_image(request):
    id = request.session.get('id')
    profile = PatientTable.objects.get(id=id)
    
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        
        if profile_image:
            # Save the file manually
            file_name = default_storage.save(profile_image.name, ContentFile(profile_image.read()))
            profile.image = file_name  # Assuming your image field is named 'image'
            profile.save()
            
            messages.success(request, 'Profile image updated successfully.')
            return redirect('patientprofile')
        else:
            messages.error(request, 'No image selected.')
    
    return render(request, 'patient/profile.html', {'profile': profile})

@patient_required
def showdoctors(request):
    id = request.session.get('id')
    departments = DepartmentTable.objects.all()
    assign = AssignDoctor.objects.select_related('department').all()
    doctors = DoctorTable.objects.all()
    medicalhistory = MedicalHistory.objects.filter(patient=id)
    return render(request, 'patient/Services.html', {'doctors': doctors, 'departments': departments, 'assign': assign,'medicalhistory':medicalhistory})

@patient_required
def bookappointment(request, id):
    if request.method == 'POST':
        patient_id = request.session.get('id')
        doctor = get_object_or_404(DoctorTable, id=id)
        message = request.POST.get('message', '')

        appointment = AppoinmentTable.objects.create(
            patient_id=patient_id,
            doctor_id=id,
            message=message,
            date=timezone.now().date(),
            time=timezone.now().time()
        )
        appointment.save()
        messages.success(request, 'Appointment booked successfully.')
        return redirect('showmyappointments')
    else:
        return render(request, 'patient/Services.html', {'id': id})

@patient_required
def showmyappointments(request):
    patient_id = request.session.get('id')
    appointments = AppoinmentTable.objects.filter(patient_id=patient_id)
    
    appointment_data = []
    for appointment in appointments:
        prescriptions = Prescribition.objects.filter(appoinmenet=appointment)
        
        # For each prescription, check if there is an associated payment
        prescription_data = []
        for prescription in prescriptions:
            has_payment = payment.objects.filter(prescription=prescription).exists()
            prescription_data.append((prescription, has_payment))
        
        appointment_data.append((appointment, prescription_data))
    
    return render(request, 'patient/Appointments.html', {'appointment_data': appointment_data})


@patient_required
def cancelappointment(request, id):
    appointment = get_object_or_404(AppoinmentTable, id=id)
    appointment.delete()
    messages.success(request, 'Appointment canceled successfully.')
    return redirect('showmyappointments')

@patient_required
def download_prescription(request, appointment_id):
    appointment = get_object_or_404(AppoinmentTable, id=appointment_id)
    prescriptions = Prescribition.objects.filter(appoinmenet=appointment)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prescriptions_{appointment_id}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 24)
    p.drawString(30, height - 40, "E-Hospitality")

    # Subheading
    p.setFont("Helvetica-Bold", 18)
    p.drawString(30, height - 70, "Prescriptions")

    # Draw a line under the heading
    p.line(30, height - 75, width - 30, height - 75)

    y = height - 90
    for prescription in prescriptions:
        if y < 100:
            p.showPage()
            y = height - 40
            p.setFont("Helvetica-Bold", 24)
            p.drawString(30, height - 40, "E-Hospitality")
            p.setFont("Helvetica-Bold", 18)
            p.drawString(30, height - 70, "Prescriptions")
            p.line(30, height - 75, width - 30, height - 75)

        p.setFont("Helvetica-Bold", 12)
        p.drawString(30, y, f"Doctor: {prescription.appoinmenet.doctor.first_name} {prescription.appoinmenet.doctor.last_name}")
        y -= 14
        p.setFont("Helvetica", 12)
        p.drawString(30, y, f"Title: {prescription.title}")
        y -= 14
        p.drawString(30, y, f"Prescription: {prescription.prescription}")
        y -= 14
        p.drawString(30, y, f"Date: {prescription.created_at}")
        y -= 28
        p.line(30, y, width - 30, y)
        y -= 14

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    return response

@patient_required
def create_update_medical_history(request):
    patient_id = request.session.get('id')
    patient = PatientTable.objects.get(id=patient_id)
    try:
        medical_history = MedicalHistory.objects.get(patient=patient)
        is_update = True
    except MedicalHistory.DoesNotExist:
        medical_history = None
        is_update = False

    if request.method == 'POST':
        family_tree = request.POST.get('FamilyTree')
        symptoms = request.POST.get('symptoms')
        taking_medication = request.POST.get('takingMedication')
        list_medication = request.POST.get('listmedication')
        medication_allergies = request.POST.get('medicationAllergies')
        use_tobacol = request.POST.get('usetobacol')
        alcohol = request.POST.get('alcohol')

        if is_update:
            medical_history.FamilyTree = family_tree
            medical_history.symptoms = symptoms
            medical_history.takingMedication = taking_medication
            medical_history.listmedication = list_medication
            medical_history.medicationAllergies = medication_allergies
            medical_history.usetobacol = use_tobacol
            medical_history.alcohol = alcohol
            medical_history.date = timezone.now().date()
            medical_history.time = timezone.now().time()
            medical_history.save()
        else:
            medical_history = MedicalHistory(
                patient=patient,
                FamilyTree=family_tree,
                symptoms=symptoms,
                takingMedication=taking_medication,
                listmedication=list_medication,
                medicationAllergies=medication_allergies,
                usetobacol=use_tobacol,
                alcohol=alcohol,
                date=timezone.now().date(),
                time=timezone.now().time(),
            )
            medical_history.save()
        return redirect('patientprofile')

    context = {
        'patient': patient,
        'medical_history': medical_history,
    }
    return render(request, 'patient/create_medical_history.html', context)

@patient_required
def initiate_payment(request, prescription_id):
    prescribition = get_object_or_404(Prescribition, id=prescription_id)
    
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        card_holder_name = request.POST.get('card_holder_name')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Assuming the payment is manually verified and successful
        payment.objects.create(
            prescription=prescribition,
            amount=5000,  # $50.00
            card=card_number,
            date=timezone.now().date(),
            time=timezone.now().time(),
        )
        
        messages.success(request, 'Payment successful!')
        return redirect('payment_success', prescription_id=prescription_id)
    
    return render(request, 'patient/payment.html', {'prescription': prescribition})


@patient_required
def payment_success(request, prescription_id):
    prescribition = get_object_or_404(Prescribition, id=prescription_id)
    messages.success(request, 'Payment was successful!')
    return render(request, 'patient/success.html', {'prescription': prescribition})


@patient_required
def payment_cancel(request):
    messages.error(request, 'Payment was canceled.')
    return render(request, 'patient/cancel.html')

@patient_required
def download_bill(request, prescription_id):
    # Fetch the prescription details
    prescription = get_object_or_404(Prescribition, id=prescription_id)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{prescription_id}.pdf"'

    # Create the PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Add custom title and styling
    p.setFont("Helvetica-Bold", 22)
    p.setFillColor(colors.HexColor("#2E86C1"))
    p.drawCentredString(width / 2.0, 770, "E-Hospitality")

    # Add bill details
    p.setFont("Helvetica", 16)
    p.setFillColor(colors.black)
    p.drawString(100, 730, f"Bill for Prescription #{prescription_id}")
    p.drawString(100, 710, f"Doctor: {prescription.appoinmenet.doctor.first_name} {prescription.appoinmenet.doctor.last_name}")
    p.drawString(100, 690, f"Date: {prescription.appoinmenet.date}")
    p.drawString(100, 670, "Total Amount: $50.00")

    # Draw a line for emphasis
    p.setLineWidth(1)
    p.line(50, 660, 550, 660)

    # Footer
    p.setFont("Helvetica-Oblique", 12)
    p.setFillColor(colors.gray)
    p.drawString(100, 640, "Thank you for choosing E-Hospitality for your healthcare needs!")

    # Finalize the PDF
    p.showPage()
    p.save()

    return response