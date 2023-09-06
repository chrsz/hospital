from io import BytesIO
from datetime import datetime

from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from appointments.excel import ExportWorkbook
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


class ExportAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        doctors = self._retrieve_doctors()
        patients = self._retrieve_patients()
        appointments = self._retrieve_appointments()

        wb = ExportWorkbook()
        wb.remove_all_sheets()

        wb.doctors.hide_excess_columns = False
        wb.doctors.write(objects=doctors)

        wb.patients.hide_excess_columns = False
        wb.patients.write(objects=patients)

        wb.appointments.hide_excess_columns = False
        wb.appointments.write(objects=appointments)

        now = datetime.now()
        filename = f'export_{now.date()}.xlsx'
        # filename = f'export_{now.date()}T{now.time()}Z.xlsx'

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        response = FileResponse(buffer, filename=filename, as_attachment=True)

        return response


    def _retrieve_doctors(self, doctors=[]):

        if not doctors:
            doctors = Doctor.objects.all()

        rows = []
        for doctor in doctors:
            row = [
                doctor.id,
                doctor.name,
                doctor.surname,
                doctor.tax_code,
            ]
            rows.append(row)

        return rows


    def _retrieve_patients(self, patients=[]):

        if not patients:
            patients = Patient.objects.all()

        rows = []
        for patient in patients:
            row = [
                patient.id,
                patient.name,
                patient.surname,
                patient.tax_code,
            ]
            rows.append(row)

        return rows


    def _retrieve_appointments(self, appointments=[]):

        if not appointments:
            appointments = Appointment.objects.all()

        rows = []
        for appointment in appointments:
            row = [
                appointment.id,
                f'{appointment.doctor.name} {appointment.doctor.surname}',
                f'{appointment.patient.name} {appointment.patient.surname}',
                appointment.date_from,
                appointment.date_to,
                appointment.notes or ' ',
            ]
            rows.append(row)

        return rows
