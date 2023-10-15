from datetime import date
from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login

from django.views.decorators.cache import never_cache





from .models import User,Patient,Woreda,Appointment,Doctor
from .forms import AddAppointement
from tests.models import LabTestOrder,PatientPaymentHistory

from .decorators import admin_required, receptionist_required, nurse_required, doctor_required, lab_technician_required, radiologist_required

# my customized login view to redirect the users to their respective home page
class CustomLoginView(LoginView):
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.role == User.Role.DOCTOR:
                login(self.request, user)
                return redirect('doctor-home')  
            elif user.role == User.Role.NURSE:
                login(self.request, user)
                return redirect('nurse')  
            elif user.role == User.Role.RECEPTION:
                login(self.request,user)
                return redirect('reception')
            elif user.role == User.Role.LAB_TECHNICIAN:
                login(self.request,user)
                return redirect('lab-tech')
            elif user.role == User.Role.ADMIN:
                login(self.request,user)
                return redirect('admin-home')
            else:
                return redirect('login')  
        else:
            form.add_error(None, 'Authentication failed. Please check your credentials.')
            return self.form_invalid(form)
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    # this function used to ensure that if a user request for login page after login the user will be redirected to their respective page(home page)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == User.Role.DOCTOR:
                return redirect('doctor-home')
            elif request.user.role == User.Role.NURSE:
                return redirect('nurse')
            elif request.user.role == User.Role.RECEPTION:
                return redirect('reception')
            elif request.user.role == User.Role.LAB_TECHNICIAN:
                return redirect('lab-tech')
            elif request.user.role == User.Role.ADMIN:
                return redirect('admin-home')
            else:
                return redirect('login')
        return super().get(request, *args, **kwargs)


# addin appointment and also check if there is validation error that if patient has active appoitment before
@login_required
@receptionist_required
def add_appointment(request):
    if request.method == "POST":
        form = AddAppointement(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(id = form.cleaned_data['patient_id'])
            doctor =  form.cleaned_data['doctor']
            fee = form.cleaned_data['appointment_fee']
            try:
                appointment = Appointment(patient = patient,doctor = doctor,appointment_fee =fee)
                appointment.save()
                payment = PatientPaymentHistory.objects.create(appointment = appointment,amount = fee,payment_reason = "Appointmet Payment")
                payment.save()
                messages.success(request,f"Appointment is succefully created for {patient.first_name} {patient.last_name}")
                return redirect('appointments')
            except ValidationError as e:
                error_message = str(e)
                return render(request, 'users/error.html', {'error_message': error_message})
            print(patient.first_name,doctor.username)
    else:
        form = AddAppointement(initial={'appointment_date': date.today(),'appointment_fee':100})
    return render(request,'users/add-appointment.html',{"form":form})

# list of patients for the receptionst
@login_required
@receptionist_required
def all_patient(request):
    patients = Patient.objects.all()
    return render(request,'users/patients.html',{"patients":patients})

@login_required
@receptionist_required
def all_appointment(request):
    appointments = Appointment.objects.all()
    return render(request,'users/appointments.html',{"appointments":appointments})

# appointments for doctor
@login_required
@doctor_required
def docotr_appointment(request):
    appointments = Appointment.objects.all()
    return render(request,'users/doctor-appointments.html',{"appointments":appointments})

@login_required
@doctor_required
def docotr_active_appointment(request):
    appointments = Appointment.objects.filter(is_active = True)
    return render(request,'users/doctor-active-appointment.html',{"appointments":appointments})

# reception home page
@login_required
@receptionist_required
@never_cache
def reception(request):
    all_patients = Patient.objects.all().count()
    all_appointments = Appointment.objects.all().count()
    active_appointments = Appointment.objects.filter(is_active = True)

    today = date.today()
    payments = PatientPaymentHistory.objects.filter(payment_date__date=today)
    sum = 0
    for payment in payments:
        sum = sum + payment.amount
    
    

    return render(request,'users/reception-home.html',{"all_patients":all_patients,"all_appointments":all_appointments,'active_appointments':active_appointments,"sum":sum,'today':today})

# nurse home page
@login_required
@nurse_required
def nurse_home(request):
    return render(request,'users/reception-home.html')
 
 #doctor home page
@login_required
@doctor_required
def doctor_home(request):
    active_appointments = Appointment.objects.filter(is_active = True)
    return render(request,'users/doctor_home.html',{'active_appointments':active_appointments})

@login_required
@lab_technician_required
def lab_tech_home(request):
    paid_orders = LabTestOrder.objects.filter(
    order_status='Paid',
    appointment__patient__isnull=False)
    patients = Patient.objects.filter(id__in=paid_orders.values('appointment__patient'))
    return render(request,'tests/lab-tech-home.html',{"patients":patients})

@login_required
@receptionist_required
def register_patient(request):
    if request.method == "POST":
        fname = request.POST.get('patient-first-name')
        lname = request.POST.get('patient-last-name')
        phone_number = request.POST.get('phone')
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        woreda = request.POST.get("woreda")

        Patient.objects.create(first_name = fname,last_name = lname,age = age,gender = gender,contact_number = phone_number,woreda = Woreda.objects.get(id = woreda))

        messages.success(request,f"{fname} { lname } pateint is created succeffuly")
        url = reverse('patients')
        return redirect(url)
    return render(request,'users/add-patient.html')


@login_required
@receptionist_required
# function to update patient data
def update_patient(request,pk):
    patient = Patient.objects.get(id = pk)
    if request.method == "POST":
        fname = request.POST.get('patient-first-name')
        lname = request.POST.get('patient-last-name')
        phone_number = request.POST.get('phone')
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        woreda = request.POST.get("woreda")
        
        patient.first_name = fname
        patient.last_name =  lname
        patient.contact_number = phone_number
        patient.age = age
        patient.gender = gender
        patient.woreda = Woreda.objects.get(id = woreda)
        patient.save()
        messages.success(request,f"{fname} { lname } record is updated succeffuly")
        url = reverse('patients')
        return redirect(url)
    return render(request,'users/update-patient.html',{'patient':patient})
    
def delete_patient(request,pk):
    patient = Patient.objects.get(id = pk)
    patient.delete()
    messages.success(request,f"{patient.first_name} {patient.last_name} has been Deleted Succefully")
    url = reverse('patients')
    return redirect(url)