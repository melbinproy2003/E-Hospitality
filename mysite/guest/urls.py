from django.urls import path
from . import views

urlpatterns = [
    path("",views.loginpage,name="login"),
    path("PatientRegistration/",views.patientregistration,name="Patientregistration"),
    path("WebadminHome/",views.webadmin,name='webadmin'),
    path("DoctorHome/",views.doctor,name='doctor'),
    path("PatientHome/",views.patient,name='patient'),
    path('logout/', views.logout_view, name='logout'),
]