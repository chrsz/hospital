from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from appointments.models import Doctor, Patient, Appointment
from appointments.api.serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all().order_by('-id')
    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticated, )


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all().order_by('-id')
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated, )


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all().order_by('-date_from')
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated, )
