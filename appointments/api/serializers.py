# from django.db.models import Q
from rest_framework import serializers

from appointments.models import Doctor, Patient, Appointment


# Serializer JSON con i campi id, nome e cognome
class DoctorSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ('id', 'name', 'surname')


# Serializer JSON con tutti i campi del modello
class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'


# Serializer JSON con tutti i campi del modello
class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = '__all__'


# Serializer JSON con esclusi i campi created_at e updated_at
# doctor_fields e patient_fields ereditano i relativi serializer per mostrare più dati oltre l'id della fk (solo in lettura)
# date_from e date_to vengono visualizzati nel formato giorno/mese/anno ora:minuti
# la funzione validate() controlla che date_to sia maggiore di date_from e che non ci siano altri appuntamenti in quel range orario
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
