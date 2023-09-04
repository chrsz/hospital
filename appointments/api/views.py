from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from appointments.models import Doctor, Patient, Appointment
from appointments.api.serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer
from appointments.api.filters import AppointmentFilter


# Vista per la creazione, aggiornamento ed eliminazione dei Dottori
# ordinati per id decrescente
# ricerca tramite &search= sui campi name, surname e tax_code
class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all().order_by('-id')
    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'surname', 'tax_code')


# Vista per la creazione, aggiornamento ed eliminazione dei Pazienti
# ordinati per id decrescente
# ricerca tramite &search= sui campi name, surname e tax_code
class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all().order_by('-id')
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'surname', 'tax_code')


# Vista per la creazione, aggiornamento ed eliminazione degli appuntamenti
# ordinati per date_from crescente
# ricerca tramite &search= sui campi name, surname e tax_code sia del dottore sia del paziente
# ricerca sempre tramite &search= anche sul campo note
# filtro direttamente tramite id del dottore e del paziente
# filtro direttamente per date (vedere AppointmentFilter in filters.py)
class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all().order_by('date_from')
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (SearchFilter, DjangoFilterBackend, )
    filterset_class = AppointmentFilter
    search_fields = (
        'doctor__name', 'doctor__surname', 'doctor__tax_code',
        'patient__name', 'patient__surname', 'patient__tax_code',
        'notes',
    )
