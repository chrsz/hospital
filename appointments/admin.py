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
    list_display = ('doctor', 'patient', 'date_from', 'date_to', 'notes')
    search_fields = (
        'doctor__name', 'doctor__surname', 'doctor__tax_code',
        'patien__name', 'patient__surname', 'patient__tax_code',
        'notes'
    )
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = [
        (
            'Appuntamento',
            {
                'fields': ('doctor', 'patient'),
            },
        ),
        (
            'Data, orario ed eventuali note',
            {
                'fields': ('date_from', 'date_to', 'notes'),
            },
        ),
        (
            'Database',
            {
                'classes': ('collapse', ),
                'fields': ('created_at', 'updated_at'),
            },
        ),
    ]
