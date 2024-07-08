from django.shortcuts import render, redirect
from django.contrib import messages
from guest.models import PatientTable
from Webadmin.models import DoctorTable, DepartmentTable, AssignDoctor
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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