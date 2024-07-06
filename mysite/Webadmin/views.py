from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DoctorTable, DepartmentTable
from guest.models import loginTable

# Create your views here.
def doctorregistration(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dob = request.POST['dob']
        specialized = request.POST['specialized']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if not loginTable.objects.filter(email=email).exists():
                doctor = DoctorTable(
                    first_name=firstname,
                    last_name=lastname,
                    dob=dob,
                    specialized=specialized,
                    email=email,
                    password=password
                )
                login = loginTable(
                    username=firstname,
                    email=email,
                    password=password,
                    type='doctor'
                )

                doctor.save()
                login.save()
                messages.success(request, 'Registration Success')
            else:
                messages.error(request, 'Email already registered')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'webadmin/AddDoctor.html')

def doctorslist(request):
    doctors = DoctorTable.objects.all()
    return render(request, 'webadmin/DoctorList.html', {'doctors': doctors})

def departments(request):
    if request.method == 'POST':
        name = request.POST['name']

        if not DepartmentTable.objects.filter(name=name).exists():
            dep = DepartmentTable(name=name)
            dep.save()
            messages.success(request, 'Department added successfully')
        else:
            messages.error(request, 'Department already exists')

    return render(request, 'webadmin/AddDepartments.html')
