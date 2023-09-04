from django.urls import include, path
from rest_framework import routers

from appointments.api.views import DoctorViewSet, PatientViewSet, AppointmentViewSet


router = routers.DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
