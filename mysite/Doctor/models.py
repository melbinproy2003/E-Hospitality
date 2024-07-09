from django.db import models
from django.utils import timezone
from Patient.models import AppoinmentTable

# Create your models here.
class Prescribition(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    time = models.TimeField(default=timezone.now().time())
    appoinmenet = models.ForeignKey(AppoinmentTable, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    prescription = models.TextField(max_length=500)

    def __str__(self):
        return self.title