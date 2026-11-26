from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models #from .models import * ou from AccountApp import doctors, patients 
from django.utils import timezone

# Create your models here.

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    doctor = models.ForeignKey("AccountApp.Doctor", related_name="appointments", on_delete=models.CASCADE)
    patient = models.ForeignKey("AccountApp.Patient", related_name="appointments", on_delete=models.CASCADE)
    
    appointment_date = models.DateField()
    reason = models.TextField(max_length=200)
    prescription = models.FileField(
        upload_to="prescriptions/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING)
    #status = models.CharField(max_length=10, choices=[("PENDING", "En attente"), (Status.CONFIRMED, "Confirmé"), (Status.CANCELLED, "Annulé")], default=Status.PENDING)
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self): #validateur coté bd
       modified_date=self._state.adding or (
            Appointment.objects.filter(
               pk=self.pk,
               appointment_date=self.appointment_date)
               .exists()
        )
       if self.appointment_date <= timezone.localdate():
           raise ValidationError("La date du rendez-vous doit être postérieure à maintenant.")
        
    class Meta:
        ordering = ["appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
                violation_error_message="on peut pas avoir deux rendez-vous pour le même médecin à la même date et heure.",
            )
        ]