from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

# Create your models here.

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    doctor = models.ForeignKey("AccountApp.Doctor", on_delete=models.CASCADE)
    patient = models.ForeignKey("AccountApp.Patient", on_delete=models.CASCADE)
    
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    prescription = models.FileField(
        upload_to="prescriptions/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING)
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        old = Appointment.objects.filter(pk=self.pk).first()
        # Si la date n'a pas changé
        if old and old.appointment_date == self.appointment_date:
            return
        # Sinon (création ou date modifiée) la date doit être dans le futur
        if self.appointment_date and self.appointment_date <= timezone.now():
            raise ValidationError("La date du rendez-vous doit être postérieure à maintenant.")
        
    class Meta:
        ordering = ["appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
            )
        ]