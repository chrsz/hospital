# from django.db.models import Q
from rest_framework import serializers

from appointments.models import Doctor, Patient, Appointment


class DoctorSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ('id', 'name', 'surname')


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_fields = DoctorSimpleSerializer(source='doctor', read_only=True)
    patient_fields = PatientSerializer(source='patient', read_only=True)
    date_from = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    date_to = serializers.DateTimeField(format='%d/%m/%Y %H:%M')

    class Meta:
        model = Appointment
        exclude = ('created_at', 'updated_at')

    def validate(self, attrs):
        doctor = attrs['doctor']
        date_from = attrs['date_from']
        date_to = attrs['date_to']

        if date_to < date_from:
            raise serializers.ValidationError({'date_to': 'The date_to needs to be higher than date_from'})

        appointment = Appointment.objects.filter(
            doctor=doctor,
            date_from__gte=date_from, date_to__lte=date_to,
        )
        appointment_count = appointment.count()

        if appointment_count > 0:
            raise serializers.ValidationError(f'There are already {appointment_count} appointments in this dates range.')

        return attrs
