from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import loginTable, PatientTable
from Webadmin.models import DoctorTable

# Create your views here.
def webadmin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.session.get('type') != 'webadmin':
            return redirect('login')  # Redirect to the login page if not 'webadmin'
        return view_func(request, *args, **kwargs)
    return wrapper_func

def doctor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.session.get('type') != 'doctor':
            return redirect('login')  # Redirect to the login page if not 'webadmin'
        return view_func(request, *args, **kwargs)
    return wrapper_func

def patient_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.session.get('type') != 'patient':
            return redirect('login')  # Redirect to the login page if not 'webadmin'
        return view_func(request, *args, **kwargs)
    return wrapper_func

def patientregistration(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dob = request.POST['dob']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if not loginTable.objects.filter(email=email).exists():
                patient = PatientTable(
                    first_name=firstname,
                    last_name=lastname,
                    dob=dob,
                    email=email,
                    password=password
                )
                login = loginTable(
                    username=firstname,
                    email=email,
                    password=password,
                    type='patient'
                )

                patient.save()
                login.save()
                messages.success(request, 'Registration Success')
                return redirect('login')
            else:
                messages.error(request, 'Email already registered')
        else:
            messages.error(request, 'Passwords do not match')
            
    return render(request, 'guest/PatientRegistration.html')

def loginpage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = loginTable.objects.get(email=email, password=password)
            request.session['username'] = user.username
            
            if user.type == 'webadmin':
                request.session['type'] = "webadmin"
                return redirect("webadmin")
            elif user.type == 'doctor':
                try:
                    doctor = DoctorTable.objects.get(email=email)
                    request.session['id'] = doctor.id
                    request.session['type'] = "doctor"  # Set the session type to 'doctor'
                    return redirect('doctor')
                except DoctorTable.DoesNotExist:
                    messages.error(request, 'Doctor not found')
            elif user.type == 'patient':
                try:
                    patient = PatientTable.objects.get(email=email)
                    request.session['id'] = patient.id
                    request.session['type'] = "patient"
                    return redirect('patient')
                except PatientTable.DoesNotExist:
                    messages.error(request, 'Patient not found')
        except loginTable.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    return render(request, "guest/login.html")

@webadmin_required
def webadmin(request):
    type = request.session.get('type')
    return render(request, 'webadmin/Home.html', {'type': type})

@doctor_required
def doctor(request):
    id = request.session.get('id')
    type = request.session.get('type')
    return render(request, 'doctor/Home.html', {'id': id,'type': type})

@patient_required
def patient(request):
    id = request.session.get('id')
    type = request.session.get('type')
    return render(request, 'patient/Home.html', {'id': id,'type': type})

def logout_view(request):
    # Clear the session
    request.session.flush()

    # Create a new session
    request.session = SessionStore()

    # Redirect the user to the login page
    return HttpResponseRedirect(reverse_lazy('login'))