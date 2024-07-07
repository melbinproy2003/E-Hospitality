from django.urls import path
from . import views

urlpatterns = [
    path("doctorregistration/",views.doctorregistration,name='doctorregistration'),
    path("doctorslist/",views.doctorslist,name="doctorslist"),
    path("newdepartments/",views.departments,name="newdepartments"),
    path("departmentlist/",views.departmentlist,name="departmentlist"),
    path("patientlist/",views.patientlist,name="patientlist"),
]