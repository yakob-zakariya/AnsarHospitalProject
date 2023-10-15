from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from datetime import date
from django.core.exceptions import ValidationError

class Region(models.Model):
    region_name = models.CharField(max_length=50)
    class Meta:
        db_table= 'Region'
        ordering = ["region_name"]
    def __str__(self):
        return self.region_name
    
class Zone(models.Model):
    zone_name = models.CharField(max_length=50)
    region = models.ForeignKey(Region,on_delete=models.CASCADE)
    class Meta:
        db_table  = 'Zone'
    
    def __str__(self):
        return self.zone_name
    
class Woreda(models.Model):
    woreda_name = models.CharField(max_length = 50)
    zone = models.ForeignKey(Zone,on_delete=models.CASCADE)
    class Meta:
        db_table = 'Woreda'
        ordering = ['woreda_name']
    
    def __str__(self):
        return self.woreda_name


class Patient(models.Model):
    GENDER = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    contact_number = models.CharField(max_length=20)
    woreda = models.ForeignKey(Woreda, on_delete=models.CASCADE)
    class Meta:
        db_table = "Patient"
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.id} -- {self.first_name} {self.last_name}"
    

class User(AbstractUser):
    
    class Role(models.TextChoices):
        ADMIN = "ADMIN","Admin"
        RECEPTION = "RECEPTION","Reception"
        NURSE = "NURSE","Nurse"
        DOCTOR = "DOCTOR","Doctor"
        LAB_TECHNICIAN= "LABIST","lab Technician"
        RADIOLOGIST = "RADIOLOGITS","Radiologist"
        

    base_role = Role.ADMIN
    role = models.CharField(max_length=50,choices=Role.choices)

    def save(self,*args,**kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args,**kwargs)
    class Meta:
        db_table = 'User'


class ReceptionManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role = User.Role.RECEPTION)

class Reception(User):
    base_role = User.Role.RECEPTION
    # objects = ReceptionManager()
    class Meta:
        proxy = True
        
class NurseManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role = User.Role.NURSE)

class Nurse(User):
    base_role = User.Role.NURSE
    # objects = NurseManager()
    class Meta:
        proxy = True

class DoctorManager(BaseUserManager):
     def get_queryset(self,*args,**kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role = User.Role.DOCTOR)
    
class Doctor(User):
    base_role = User.Role.DOCTOR
    # objects = DoctorManager()
    class Meta:
        proxy = True


class LabTechnicianManager(BaseUserManager):
     def get_queryset(self,*args,**kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role = User.Role.LAB_TECHNICIAN)
    
class LabTecnician(User):
    base_role = User.Role.LAB_TECHNICIAN
    # objects = LabTechnicianManager()
    class Meta:
        proxy = True

class RadiologistManager(BaseUserManager):
     def get_queryset(self,*args,**kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role = User.Role.RADIOLOGIST)
    
class Radiologist(User):
    base_role = User.Role.RADIOLOGIST
    # objects = RadiologistManager()
    class Meta:
        proxy = True

# 1 patient can have only active appointment at a time
class Appointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    appointment_date = models.DateField(default=date.today)
    appointment_fee = models.FloatField()
    appointment_status = models.CharField(max_length=50, default='Nurse Ques')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Check if the patient have already active appointment
        
        existing_active_appointment = Appointment.objects.filter(
            patient=self.patient,
            is_active=True
        ).exclude(pk=self.pk)  # Exclude the current instance if it's being updated

        if existing_active_appointment.exists():
            raise ValidationError("Patient already has an active appointment.")

        super(Appointment, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'Appointment'
        ordering = ['-appointment_date']

    def __str__(self):
        return f"{self.patient.id}--{self.patient.first_name} {self.patient.last_name} "
