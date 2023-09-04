import django_filters as filters

from appointments.models import Appointment


# Creazione filtro custom in GET con possibilità di filtrare per date
class AppointmentFilter(filters.FilterSet):
    date_from = filters.IsoDateTimeFilter(field_name='date_from', lookup_expr='gte')
    date_to = filters.IsoDateTimeFilter(field_name='date_to', lookup_expr='lte')

    class Meta:
        model = Appointment
        fields = ('doctor', 'patient', 'date_from', 'date_to')
