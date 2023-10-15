from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from .models import LabTestOrder,LabTestPayment,LabTestResult,Sample,PatientPaymentHistory,VitalRegistration
from users.models import Patient,Doctor,Appointment
from users.decorators import lab_technician_required,doctor_required,receptionist_required
from .forms import LabTestOrderForm
from django.contrib.auth.decorators import login_required

import qrcode
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseRedirect


# filling the lab test using check boxes from the form and appointment id (by passing it through template)
@login_required
@doctor_required
def fill_lab_test_order(request,pk):
    patient = Patient.objects.get(appointment__id = pk)
    patient_id = patient.id

    if request.method == 'POST':
        form = LabTestOrderForm(request.POST)
        if form.is_valid():
            appointment = Appointment.objects.get(id = pk)
            selected_lab_tests = form.cleaned_data['lab_tests']
            
            # to fill the doctor fields get it from the request because this view is only be accessible with doctors that have the account
            doctor = Doctor.objects.get(id = request.user.id)
            # Create LabTestOrder instances for each selected lab test
            for lab_test in selected_lab_tests:
                LabTestOrder.objects.create(
                    appointment_id=appointment.id,
                    labtest=lab_test,
                    doctor=doctor,
                )
            messages.success(request,f"Lab test order is created succefully {patient.first_name} {patient.last_name} ")
            url = reverse('tests:patient-history', args=[patient_id])
            return  redirect(url)
    else:
        form = LabTestOrderForm()
        
    return render(request, 'tests/labtest_order.html', {'form': form,'patient':patient})


# to get the list of pending patient for Reception
@login_required
@receptionist_required
def pending_patients(request):

    pending_orders = LabTestOrder.objects.filter(
    order_status='Pending',
    appointment__patient__isnull=False)
    patients = Patient.objects.filter(id__in=pending_orders.values('appointment__patient'))
    return render(request,'tests/pending.html',{'patients':patients})

@login_required
def patient_detail(request,pk):
    pending_orders = LabTestOrder.objects.filter(order_status = 'Pending',appointment__patient_id = pk)
    paid_orders = LabTestOrder.objects.filter(order_status = "Paid",appointment__patient_id = pk)
    patient = Patient.objects.get(id = pk)
    total_price = 0
    for order in pending_orders:
        total_price = total_price + order.labtest.price
        
    return render(request,'tests/detail.html',{'pending_orders':pending_orders,'total':total_price,"patient":patient,'paid_orders':paid_orders})

@login_required
@receptionist_required
def payLab(request,pk):
    pending_orders = LabTestOrder.objects.filter(order_status = 'Pending',appointment__patient_id = pk)
    total_price = 0
    url = reverse('tests:patient-detail', args=[pk])
    for order in pending_orders:
        payment = LabTestPayment(labtest_order = order,price=order.labtest.price,patient=order.appointment.patient)
        payment.save()
        order.order_status = "Paid"
        order.save()
        total_price = total_price + float(order.labtest.price)
    appointment = Appointment.objects.get(patient_id = pk,is_active = True)
    payment = PatientPaymentHistory.objects.create(appointment = appointment,amount = total_price,payment_reason = "Lab Payment")
    return redirect(url)
@login_required
@lab_technician_required
def paid_orders(request,pk):
    paid_orders = LabTestOrder.objects.filter(order_status = "Paid",appointment__patient_id = pk)
    patient= Patient.objects.get(id = pk)
    appointment = Appointment.objects.get(patient_id = patient,is_active = True)
    sample = Sample.objects.filter(appointment = appointment)

    return render(request,'tests/paid-orders.html',{'paid_orders':paid_orders,'patient':patient,'sample':sample})

@login_required

def pending_lab(request):
    pending_orders = LabTestOrder.objects.filter(
    order_status='Pending',
    appointment__patient__isnull=False)
    patients = Patient.objects.filter(id__in=pending_orders.values('appointment__patient'))
    return render(request,'tests/pending-lab-tech.html',{'patients':patients})

@login_required
@lab_technician_required
def fill_lab_result(request,pk):
    patient = Patient.objects.get(appointment__labtestorder__id = int(pk))
    labtestorder = LabTestOrder.objects.get(id = pk)
    
    
    if request.method == "POST":
        result = request.POST['result']
        result_comment = request.POST['result_comment']
        LabTestResult.objects.create(labtestorder = labtestorder,lab_technician= request.user,result  = result,result_comment = result_comment )
        labtestorder.order_status = "Lab completed"
        labtestorder.save()
        
        url = reverse('tests:paid-orders', args=[patient.id])
        return redirect(url)   
    else:
        return render(request,'tests/result.html',{'patient':patient,'labtestorder':labtestorder})

def lab_result(request):
    # results = LabTestResult.objects.all()
    pass

@login_required
@receptionist_required
def all_patient_dr(request):
    patients = Patient.objects.all()
    return render(request,'tests/patient-dr.html',{"patients":patients})
   
@login_required
def patient_history(request,pk):
    patient = Patient.objects.get(id = pk)
    results = LabTestResult.objects.filter(labtestorder__appointment__patient_id = pk)
    Vital = VitalRegistration.objects.filter(appointment__patient_id = pk,appointment__is_active = True)
    return render(request,'tests/patient-history.html',{"patient":patient,"results":results,"vital":Vital})

@login_required
@lab_technician_required
def generateQrCode(request,pk):
    patient = Patient.objects.get(id = pk)
    appointment = Appointment.objects.get(patient_id=pk,is_active = True)
    
    data =  f"Patient ID : {patient.id}\nAppointment ID: {appointment.id}\nFull Name:{appointment.patient.first_name} {appointment.patient.last_name}\nDate sample taken: {appointment.appointment_date}"
    
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,)
    
    
    qr.add_data(data)
    qr.make(fit=True)
    qr_code = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    qr_code.save(buffer, format="PNG")
    image_data = buffer.getvalue()
    buffer.close()

    # Create a SimpleUploadedFile from the image data
    qr_code_file = SimpleUploadedFile(f"sample_{appointment.id}_qr.png", image_data, content_type="image/png")

    sample = Sample(appointment=appointment, qr_code=qr_code_file)
    sample.save()
    messages.success(request,f"QR code is created successfully for {appointment.patient.first_name} {appointment.patient.last_name}")
    
    current_page_url = reverse('tests:paid-orders', args=[appointment.patient.id])

    return HttpResponseRedirect(current_page_url)