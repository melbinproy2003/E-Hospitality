from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
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
    departments = DepartmentTable.objects.all()
    assign = AssignDoctor.objects.select_related('department').all()
    doctors = DoctorTable.objects.all()
    return render(request, 'patient/Services.html', {'doctors': doctors, 'departments': departments, 'assign': assign})

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
    appointment_data = [(appointment, Prescribition.objects.filter(appoinmenet=appointment)) for appointment in appointments]
    bill = payment.objects.filter(prescription__appoinmenet__patient_id=patient_id)
    return render(request, 'patient/Appointments.html', {'appointment_data': appointment_data, 'bill': bill})

@patient_required
def cancelappointment(request, id):
    appointment = get_object_or_404(AppoinmentTable, id=id)
    appointment.delete()
    messages.success(request, 'Appointment canceled successfully.')
    return redirect('showmyappointments')

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
    p.setFont("Helvetica-Bold", 16)
    p.drawString(30, height - 40, "Prescriptions")
    
    y = height - 60
    for prescription in prescriptions:
        if y < 100:
            p.showPage()
            y = height - 40
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
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Consultation Fee',
                        },
                        'unit_amount': 5000,  # $50.00 in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(f'/payment_success/{prescription_id}/'),
                cancel_url=request.build_absolute_uri('/payment_cancel/'),
            )
            return redirect(session.url, code=303)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('showmyappointments')
    return render(request, 'patient/payment.html', {'prescription': prescribition})



@patient_required
def payment_success(request, prescription_id):
    prescribition = get_object_or_404(Prescribition, id=prescription_id)
    payment.objects.create(
        prescription=prescribition,
        amount=5000,  # The amount you charged
        date=timezone.now().date(),
        time=timezone.now().time(),
    )
    messages.success(request, 'Payment successful!')
    return render(request, 'patient/success.html', {'prescription': prescribition})

@patient_required
def payment_cancel(request):
    messages.error(request, 'Payment canceled.')
    return render(request, 'patient/cancel.html')