from django.contrib import admin
from .models import PatientTable, loginTable

# Register your models here.
class PatientTableAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'dob', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('dob',)

class loginTableAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'type')
    search_fields = ('username', 'email')
    list_filter = ('type',)

admin.site.register(PatientTable, PatientTableAdmin)
admin.site.register(loginTable, loginTableAdmin)
