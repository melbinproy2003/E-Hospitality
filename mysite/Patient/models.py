from django.db import models
from django.utils import timezone
class AppoinmentTable(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('guest.PatientTable', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Webadmin.DoctorTable', on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(default=timezone.now().time())

    def __str__(self):
        return str(self.id)

class MedicalHistory(models.Model):
    STATUS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    alcohol_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Never', 'Never'),
        ('Other', 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('guest.PatientTable', on_delete=models.CASCADE)
    FamilyTree = models.TextField()
    symptoms = models.TextField()
    takingMedication = models.CharField(max_length=1, choices=STATUS_CHOICES)
    listmedication = models.TextField(null=True, blank=True)
    medicationAllergies = models.CharField(max_length=1, choices=STATUS_CHOICES)
    usetobacol = models.CharField(max_length=1, choices=STATUS_CHOICES)
    alcohol = models.CharField(max_length=10, choices=alcohol_CHOICES)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(default=timezone.now().time())

    def __str__(self):
        return str(self.id)

class payment(models.Model):
    id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey('Doctor.Prescribition', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(default=timezone.now().time())

    def __str__(self):
        return str(self.id)