from django.db import models

# Create your models here.
class DoctorTable(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    image=models.ImageField(upload_to='profile',null=True,blank=True)
    specialized = models.TextField()
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class DepartmentTable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
    
class AssignDoctor(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(DoctorTable, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentTable, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doctor} {self.department}"