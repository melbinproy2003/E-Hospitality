from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from .models import DoctorTable, DepartmentTable
from guest.models import PatientTable
from guest.models import loginTable

# Create your views here.
def webadmin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.session.get('type') != 'webadmin':
            return redirect('login')  # Redirect to the login page if not 'webadmin'
        return view_func(request, *args, **kwargs)
    return wrapper_func

@webadmin_required
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
            try:
                login, created = loginTable.objects.get_or_create(
                    username=firstname,
                    email=email,
                    password=password,
                    type='doctor'
                )

                if not created:
                    messages.error(request, 'Email already registered')
                    return redirect('doctorslist')
                
                doctor = DoctorTable(
                    first_name=firstname,
                    last_name=lastname,
                    dob=dob,
                    specialized=specialized,
                    email=email,
                    password=password
                )

                doctor.save()
                login.save()
                messages.success(request, 'Registration Success')
                return redirect('doctorslist')

            except IntegrityError:
                messages.error(request, 'Email already registered')
                return redirect('doctorslist')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('doctorslist')

    return render(request, 'webadmin/Index.html')

@webadmin_required
def doctorslist(request):
    doctors = DoctorTable.objects.all()
    return render(request, 'webadmin/DoctorList.html', {'doctors': doctors})

@webadmin_required
def departments(request):
    if request.method == 'POST':
        name = request.POST['name']

        if not DepartmentTable.objects.filter(name=name).exists():
            dep = DepartmentTable(name=name)
            dep.save()
            messages.success(request, 'Department added successfully')
            return redirect('departmentlist')
        else:
            messages.error(request, 'Department already exists')
            return redirect('departmentlist')

    return render(request, 'webadmin/Index.html')

@webadmin_required
def departmentlist(request):
    department = DepartmentTable.objects.all()
    return render(request, 'webadmin/DepartmentList.html', {'departments': department})

@webadmin_required
def patientlist(request):
    patient = PatientTable.objects.all()
    return render(request,"webadmin/PatientsList.html",{'patient':patient})