from django.contrib import admin
from appointments.models import Doctor, Patient, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'tax_code')
    search_fields = ('name', 'surname', 'tax_code')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'tax_code')
    search_fields = ('name', 'surname', 'tax_code')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date_hour', 'notes')
    search_fields = (
        'doctor__name', 'doctor__surname', 'doctor__tax_code',
        'patien__name', 'patient__surname', 'patient__tax_code',
        'notes'
    )
