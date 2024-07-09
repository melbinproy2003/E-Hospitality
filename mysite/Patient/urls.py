from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile, name="patientprofile"),
    path("updatePatientProfileImage/", views.update_patient_profile_image, name="update_patient_profile_image"),
    path("showdoctors/", views.showdoctors, name="showdoctors"),  
    path("bookappointment/<int:id>/", views.bookappointment, name="bookappointment"),
    path("showmyappointments/", views.showmyappointments, name="showmyappointments"),
    path("cancelappointment/<int:id>/", views.cancelappointment, name="cancelappointment"),
    path('medicalhistory/', views.create_update_medical_history, name="medicalhistory"),
    path('download_prescription/<int:appointment_id>/', views.download_prescription, name='download_prescription'),
    path('payment/<int:prescription_id>/', views.initiate_payment, name='billpayment'),
    path('payment_success/<int:prescription_id>/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
]