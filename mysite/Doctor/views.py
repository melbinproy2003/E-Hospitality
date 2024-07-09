from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . models import Prescribition
from guest.models import PatientTable
from Webadmin.models import DoctorTable
from Patient.models import AppoinmentTable, MedicalHistory
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.
def doctor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.session.get('type') != 'doctor':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper_func

@doctor_required
def profile(request):
    id = request.session.get('id')
    profile = DoctorTable.objects.get(id=id)
    return render(request, 'doctor/profile.html', {'profile': profile, 'id': id})

@doctor_required
def update_profile_image(request):
    id = request.session.get('id')
    profile = DoctorTable.objects.get(id=id)
    
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        
        if profile_image:
            file_name = default_storage.save(profile_image.name, ContentFile(profile_image.read()))
            profile.image = file_name
            profile.save()
            
            messages.success(request, 'Profile image updated successfully.')
            return redirect('doctorprofile')
        else:
            messages.error(request, 'No image selected.')
    
    return render(request, 'doctor/profile.html', {'profile': profile})

def appointment_list(request):
    doctor_id = request.session.get('id')
    doctor = get_object_or_404(DoctorTable, id=doctor_id)
    appointments = AppoinmentTable.objects.filter(doctor_id=doctor_id)
    appointment_ids = appointments.values_list('id', flat=True)
    prescriptions = Prescribition.objects.filter(appoinmenet_id__in=appointment_ids).values_list('appoinmenet_id', flat=True)
    return render(request, 'doctor/appointment_list.html', {
        'appointments': appointments,
        'doctor': doctor,
        'prescriptions': prescriptions
    })


def complete_appointment(request):
    doctor_id = request.session.get('id')
    doctor = get_object_or_404(DoctorTable, id=doctor_id)
    # Get all completed prescriptions for the doctor
    completed_prescriptions = Prescribition.objects.filter(appoinmenet__doctor_id=doctor_id)
    # Extract the appointment IDs from the completed prescriptions
    appointment_ids = completed_prescriptions.values_list('appoinmenet_id', flat=True).distinct()
    # Get all the corresponding appointments
    appointments = AppoinmentTable.objects.filter(id__in=appointment_ids)
    return render(request, 'doctor/complete_appointment.html', {'appointments': appointments, 'doctor': doctor})


def appointment(request, id):
    data = AppoinmentTable.objects.get(id=id)
    pid = data.patient_id
    history = MedicalHistory.objects.get(patient_id=pid)
    current_prescriptions = Prescribition.objects.filter(appoinmenet_id=id)
    previous_prescriptions = Prescribition.objects.filter(appoinmenet__patient_id=pid)
    return render(request, 'doctor/appointment.html', {
        'data': data, 
        'history': history, 
        'current_prescriptions': current_prescriptions,
        'previous_prescriptions': previous_prescriptions
    })

def prescription(request, id):
    if request.method == 'POST':
        title = request.POST['title']
        prescription_text = request.POST['prescription']
        appointment = AppoinmentTable.objects.get(id=id)
        prescription = Prescribition(appoinmenet=appointment, title=title, prescription=prescription_text)
        prescription.save()
        return redirect('appointment', id=id)
    else:
        appointment = AppoinmentTable.objects.get(id=id)
        prescriptions = Prescribition.objects.filter(appoinmenet_id=id)
        return render(request, 'doctor/appointment.html', {'data': appointment, 'prescriptions': prescriptions})