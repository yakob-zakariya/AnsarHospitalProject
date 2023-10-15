from django.contrib import admin

# Register your models here.
from .models import LabTestPayment,VitalRegistration

admin.site.register(LabTestPayment)
admin.site.register(VitalRegistration)
