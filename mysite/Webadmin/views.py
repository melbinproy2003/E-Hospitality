from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Q  
from .models import DoctorTable, DepartmentTable, AssignDoctor
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
def assignDoctor(request, id):
    doctor = DoctorTable.objects.get(id=id)
    departments = DepartmentTable.objects.all()

    if request.method == 'POST':
        department_id = request.POST['department']
        department = DepartmentTable.objects.get(id=department_id)

        if not AssignDoctor.objects.filter(doctor=doctor, department=department).exists():
            assign = AssignDoctor(doctor=doctor, department=department)
            assign.save()
            messages.success(request, 'Doctor assigned successfully')
            return redirect('doctorslist')
        else:
            messages.error(request, 'Doctor already assigned to this department')

        return redirect('assigndoctor', id=doctor.id)

    return render(request, 'webadmin/DoctorList.html', {'doctor': doctor, 'departments': departments})

@webadmin_required
def doctorslist(request):
    query = request.GET.get('q', '')
    doctors = DoctorTable.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )
    assigns = AssignDoctor.objects.select_related('department').all()
    departments = DepartmentTable.objects.all()

    paginator = Paginator(doctors, 10)  # Show 10 doctors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'webadmin/DoctorList.html', {
        'page_obj': page_obj,
        'assigns': assigns,
        'departments': departments,
        'query': query,
    })

@webadmin_required
def removeDoctor(request, id):
    doctor = DoctorTable.objects.get(id=id)
    email = doctor.email
    login = loginTable.objects.get(email=email)
    login.delete()
    doctor.delete()
    return redirect('doctorslist')

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
    department_list = DepartmentTable.objects.all()
    paginator = Paginator(department_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'webadmin/DepartmentList.html', {'page_obj': page_obj})

@webadmin_required
def removeDepartment(request, id):
    department = DepartmentTable.objects.get(id=id)
    department.delete()
    return redirect('departmentlist')

@webadmin_required
def patientlist(request):
    query = request.GET.get('q')
    if query:
        patients_list = PatientTable.objects.filter(first_name__icontains=query) | PatientTable.objects.filter(last_name__icontains=query)
    else:
        patients_list = PatientTable.objects.all()

    paginator = Paginator(patients_list, 10)  # Show 10 patients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'webadmin/PatientsList.html', {
        'page_obj': page_obj,
        'query': query
    })

@webadmin_required
def removePatient(request, id):
    patient = PatientTable.objects.get(id=id)
    email = patient.email
    login = loginTable.objects.get(email=email)
    login.delete()
    patient.delete()
    return redirect('patientlist')