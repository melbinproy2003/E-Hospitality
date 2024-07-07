from django.urls import path
from . import views

urlpatterns = [
    path("doctorprofile/",views.profile,name="doctorprofile"),
    path('update_profile_image/', views.update_profile_image, name='update_profile_image'),
]