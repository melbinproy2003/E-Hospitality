from django.urls import path
from . import views

urlpatterns = [
    path("profile/",views.profile,name="patientprofile"),
    path("updatePatientProfileImage/",views.update_patient_profile_image,name="update_patient_profile_image"),
]