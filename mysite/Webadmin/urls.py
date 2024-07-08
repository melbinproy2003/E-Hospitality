from django.urls import path
from . import views

urlpatterns = [
    path("doctorregistration/",views.doctorregistration,name='doctorregistration'),
    path("doctorslist/",views.doctorslist,name="doctorslist"),
    path("assigndoctor/<int:id>/",views.assignDoctor,name="assigndoctor"),
    path("removedoctor/<int:id>/",views.removeDoctor,name="removedoctor"),
    path("newdepartments/",views.departments,name="newdepartments"),
    path("departmentlist/",views.departmentlist,name="departmentlist"),
    path("removedepartment/<int:id>/",views.removeDepartment,name="removedepartment"),
    path("patientlist/",views.patientlist,name="patientlist"),
    path("removepatient/<int:id>/",views.removePatient,name="removepatient"),
]