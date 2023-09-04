from django.contrib import admin
from appointments.models import Doctor, Patient, Appointment


# Grafica admin Django per il modello Dottore
# - mostra (e si possono cercare) i campi nome, cognome e codice fiscale
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'tax_code')
    search_fields = ('name', 'surname', 'tax_code')


# Grafica admin Django per il modello Paziente
# - mostra (e si possono cercare) i campi nome, cognome e codice fiscale
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'tax_code')
    search_fields = ('name', 'surname', 'tax_code')


# Grafica admin Django per il modello Appuntamento
# - mostra (e si possono cercare) i campi nome, cognome e codice fiscale sia del dottore sia del paziente
# - mostra (e si possono cercare) eventuali note
# - mostra data inizio e data fine appuntamento
# la pagina di dettaglio viene divisa in tre sezioni (Appuntamento, Data, orario etc..., Database)
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
