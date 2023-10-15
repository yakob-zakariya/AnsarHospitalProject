from django.db import models
from users.models import Nurse,Doctor,Patient,LabTecnician,Reception,Appointment
from datetime import date
 

class LabTest(models.Model):
    name = models.CharField(max_length = 200)
    sample_type = models.CharField(max_length = 200)
    normal_value = models.CharField(max_length = 200)
    referance_range = models.CharField(max_length = 200)
    proccessing_time = models.FloatField()
    price = models.FloatField()
    unit = models.CharField(max_length = 20)
    describtion = models.TextField()
    orders = models.ManyToManyField(
        Appointment,
        through = 'LabTestOrder',
        through_fields=("labtest","appointment"))

    class Meta:
        db_table = 'LabTest'
        ordering = ['name']
    def __str__(self):
        return self.name
    
class LabTestOrder(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    labtest = models.ForeignKey(LabTest,on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor,
        models.SET_NULL,
        blank=True,
        null = True
    )
    order_date = models.DateField(default=date.today)
    order_status = models.CharField(max_length=50,default='Pending')

    class Meta:
        db_table = 'LabTestOrder'
        ordering = ["order_date"]
    
    def __str__(self):
        return f"{self.labtest.name} for {self.appointment.patient.first_name}"
    
class LabTestPayment(models.Model):
    labtest_order = models.OneToOneField(LabTestOrder,on_delete=models.SET_NULL,null=True)
    price = models.FloatField()
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    payment_date = models.DateField(auto_now=True)
    
    class Meta:
        db_table = "LabTestPayment"
        ordering = ['payment_date']


class LabTestResult(models.Model):
    labtestorder = models.OneToOneField(LabTestOrder,on_delete = models.CASCADE)
    lab_technician = models.ForeignKey(LabTecnician,on_delete=models.CASCADE)
    result = models.TextField()
    result_comment = models.TextField()
    result_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'LabTestResult'

class VitalRegistration(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse,on_delete=models.CASCADE)
    blood_pressure = models.CharField(max_length=50)
    systolic_pressure  = models.CharField(max_length=50)
    diastolic_pressure = models.CharField(max_length=50)
    temperature = models.CharField(max_length=50)
    body_weight = models.CharField(max_length=50)
    heart_rate = models.CharField(max_length=50)
    respiratory_rate  = models.CharField(max_length=50)
    oxygen_saturation = models.CharField(max_length=50)
    date_vital_taken = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'VitalRegistration'
        ordering = ['-appointment']

class PatientPaymentHistory(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_reason = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50,default="Cash")

    class Meta:
        db_table = 'PatientPaymentHistory'
        ordering = ['payment_date']


class Sample(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    date_sample_taken = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(blank=True,upload_to='patients_QRcode')
    
    def __str__(self):
        return f"{self.appointment.patient.first_name} {self.appointment.patient.last_name} sample on{self.date_sample_taken}"
    
    class Meta:
        db_table = 'Sample'
        ordering = ['-date_sample_taken']
        
    
