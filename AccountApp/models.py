from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator,RegexValidator
from django.utils import timezone


# Create your models here.
class User (AbstractUser):
    pass  ##pas d'attributs spécifiques, il les hérite

number_validator = RegexValidator(regex=r'^\d{8}$', message="le numero de téléphone doit contenir exactement 8 chiffres.")
def birth_date_validator(date):
    if date <= timezone.now().date(): ##ou timezone.localdate()
        raise ValidationError("La date de naissance doit être antérieure à la date actuelle.")
    
class Doctor (User):
    license_number = models.CharField(max_Length=6, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    phone = models.CharField(max_length=8, validators=[number_validator])
    specialities = models.ManyToManyField("AccountApp.Speciality", related_name="doctors")

class Patient (User):
    national_id = models.CharField(max_length=8, unique=True, validators=[number_validator])
    phone = models.CharField(max_length=8, validators=[number_validator])
    birth_date = models.DateField(validators=[birth_date_validator])

class Speciality (models.Model):
    name = models.CharField(max_length=50, unique=True)
