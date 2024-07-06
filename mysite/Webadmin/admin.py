from django.contrib import admin
from .models import DoctorTable, DepartmentTable

class DoctorTableAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'specialized', 'status')
    list_filter = ('status', 'specialized')
    search_fields = ('first_name', 'last_name', 'email', 'specialized')
    ordering = ('last_name', 'first_name')

class DepartmentTableAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(DoctorTable, DoctorTableAdmin)
admin.site.register(DepartmentTable, DepartmentTableAdmin)
