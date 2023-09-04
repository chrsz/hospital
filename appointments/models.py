from django.db import models


class Person(models.Model):
    name = models.CharField('Nome', max_length=255)
    surname = models.CharField('Cognome', max_length=255)
    tax_code = models.CharField('Codice Fiscale', max_length=16, unique=True)

    class Meta:
        abstract = True


class Doctor(Person):

    class Meta:
        verbose_name = 'Dottore'
        verbose_name_plural = 'Dottori'

    def __str__(self):
        return f'[{self.id}] Dottore {self.name} {self.surname}'


class Patient(Person):

    class Meta:
        verbose_name = 'Paziente'
        verbose_name_plural = 'Pazienti'

    def __str__(self):
        return f'[{self.id}] Paziente {self.name} {self.surname}'


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, verbose_name='Dottore', on_delete=models.CASCADE, related_name='doctors')
    patient = models.ForeignKey(Patient, verbose_name='Paziente', on_delete=models.CASCADE, related_name='patients')
    date_from = models.DateTimeField('Da')
    date_to = models.DateTimeField('A')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Appuntamento'
        verbose_name_plural = 'Appuntamenti'

    def __str__(self):
        return f'[{self.id}] Appuntamento del paziente {self.patient.surname} con il dottore {self.doctor.surname}'
