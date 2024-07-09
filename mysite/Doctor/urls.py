from django.urls import path
from . import views

urlpatterns = [
    path("doctorprofile/", views.profile, name="doctorprofile"),
    path('update_profile_image/', views.update_profile_image, name='update_profile_image'),
    path("showappointments/", views.appointment_list, name="showappointments"),
    path("appointment/<int:id>/", views.appointment, name="appointment"),
    path("prescription/<int:id>/", views.prescription, name="prescription"),
    path("CompleteAppointment/", views.complete_appointment, name="CompleteAppointment"),
]
