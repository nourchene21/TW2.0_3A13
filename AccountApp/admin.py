from django.contrib import admin
from .models import User, Doctor, Patient, Specialty


# Register your models here.
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Specialty)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass