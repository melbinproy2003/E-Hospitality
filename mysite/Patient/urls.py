from django.urls import path
from . import views

urlpatterns = [
    path("profile/",views.profile,name="patientprofile"),
    path("updatePatientProfileImage/",views.update_patient_profile_image,name="update_patient_profile_image"),
    path("showdoctors/",views.showdoctors,name="showdoctors"),  
    path("appointment/<int:id>/",views.appointment,name="appointment"),
    path("showappointments/",views.showappointments,name="showappointments"),
    # path("cancelappointment/<int:id>/",views.cancelappointment,name="cancelappointment"),
    path('medicalhistory/',views.create_update_medical_history,name="medicalhistory"),
]