from django.db import models
from django.conf import settings

class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.username} with {self.doctor.username} on {self.date} at {self.time}"
