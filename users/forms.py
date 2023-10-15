from django import forms
from django.forms import ModelForm
from .models import Nurse,Doctor,Appointment
from datetime import date

class AddAppointement(ModelForm):
    patient_id = forms.IntegerField()
    doctor = forms.Select()
    appointment_fee = forms.FloatField()
    appointment_date = forms.DateField()
  
    class Meta:
        model = Appointment
        fields = ['patient_id','doctor','appointment_fee']
