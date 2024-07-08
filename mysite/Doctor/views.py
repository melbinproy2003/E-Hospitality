from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from guest.models import PatientTable
from Webadmin.models import DoctorTable
from Patient.models import AppoinmentTable
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
            # Save the file manually
            file_name = default_storage.save(profile_image.name, ContentFile(profile_image.read()))
            profile.image = file_name  # Assuming your image field is named 'image'
            profile.save()
            
            messages.success(request, 'Profile image updated successfully.')
            return redirect('doctorprofile')
        else:
            messages.error(request, 'No image selected.')
    
    return render(request, 'doctor/profile.html', {'profile': profile})

def appointment_list(request):
    doctor_id = request.session.get('id')  # Assuming 'id' in session refers to doctor id
    doctor = get_object_or_404(DoctorTable, id=doctor_id)  # Adjust DoctorTable as per your model name

    # Retrieve appointments where doctor_id matches the doctor's id from session
    appointments = AppoinmentTable.objects.filter(doctor_id=doctor_id)

    return render(request, 'doctor/appointment_list.html', {'appointments': appointments, 'doctor': doctor})
