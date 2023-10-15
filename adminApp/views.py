from django.shortcuts import render,redirect
from users.models import Reception,User
from django.contrib import messages
from django.db.models import Q
from users.decorators import admin_required
from django.contrib.auth.decorators import login_required
from users.models import Patient,Reception,Appointment,Doctor,LabTecnician
from tests.models import PatientPaymentHistory
from datetime import date
from django.views.decorators.cache import never_cache

@login_required
@admin_required
@never_cache
def home(request):
    patients = Patient.objects.all().count()
    appointments = Appointment.objects.filter(is_active = True).count()
    today = date.today()
    today_payments = PatientPaymentHistory.objects.filter(payment_date__date=today)
    payments = PatientPaymentHistory.objects.all()
    today_total = 0
    total = 0
    for payment in today_payments:
        today_total= today_total + payment.amount
    for payment in payments:
        total = total + payment.amount
        
    return render(request,'adminApp/dashboard.html',{'patients':patients,'appointments':appointments,'today_total':today_total,'total':total})

@login_required
@admin_required
def reception(request):
    if request.method == "POST":
        is_active = request.POST.get('is_active')
        is_staff = request.POST.get('is_staff')
        is_staff = int(is_staff)
        is_active = int(is_active)
        if is_active:
            is_active = True
        else:
            is_active = False
        if is_staff:
            is_staff = True
        else:
            is_staff = False
        
        receptions = User.objects.filter(role = "RECEPTION",is_active = is_active,is_staff = is_staff)
        total = receptions.count()
        print(total)
        print(receptions)
        return render(request,'adminApp/reception-user.html',{'receptions':receptions,'total':total})
    else:
        receptions = User.objects.filter(role = "RECEPTION")
        total = receptions.count()
        return render(request,'adminApp/reception-user.html',{'receptions':receptions,'total':total})


@login_required
@admin_required
def add_reception(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        
        if User.objects.filter(Q(username=username)).exists():
            return render(request, 'adminApp/error.html', {'error_message': 'Username already exists'})
        Reception.objects.create_user(username = username,password = password)
        messages.success(request,f"Account created Succefully {username}")
    
        return redirect('reception-user')
    else:
        return render(request,'adminApp/register.html',{'user':'Reception'})
    


@login_required
@admin_required
def doctor(request):
    if request.method == "POST":
        is_active = request.POST.get('is_active')
        is_staff = request.POST.get('is_staff')
        is_staff = int(is_staff)
        is_active = int(is_active)
        if is_active:
            is_active = True
        else:
            is_active = False
        if is_staff:
            is_staff = True
        else:
            is_staff = False
        
        doctors = User.objects.filter(role = "DOCTOR",is_active = is_active,is_staff = is_staff)
        total = doctors.count()
        
        return render(request,'adminApp/doctor-user.html',{'doctors':doctors,'total':total})
    else:
        doctors = User.objects.filter(role = "DOCTOR")
        total = doctors.count()
        return render(request,'adminApp/doctor-user.html',{'doctors':doctors,'total':total})



@login_required
@admin_required
def add_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        if User.objects.filter(Q(username=username)).exists():
            return render(request, 'adminApp/error.html', {'error_message': 'Username already exists'})
        Doctor.objects.create_user(username = username,password = password)
        messages.success(request,f"Account created Succefully {username}")
    
        return redirect('doctor-user')
    else:
        return render(request,'adminApp/register.html',{'user':'Doctor'})
    




@login_required
@admin_required
def lab(request):
    if request.method == "POST":
        is_active = request.POST.get('is_active')
        is_staff = request.POST.get('is_staff')
        is_staff = int(is_staff)
        is_active = int(is_active)
        if is_active:
            is_active = True
        else:
            is_active = False
        if is_staff:
            is_staff = True
        else:
            is_staff = False
        
        labs = User.objects.filter(role = "LABIST",is_active = is_active,is_staff = is_staff)
        total = labs.count()
        
        return render(request,'adminApp/lab-user.html',{'labs':labs,'total':total})
    else:
        labs = LabTecnician.objects.filter(role = "LABIST")
        total = labs.count()
        return render(request,'adminApp/lab-user.html',{'labs':labs,'total':total})



@login_required
@admin_required
def add_lab(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        if User.objects.filter(Q(username=username)).exists():
            return render(request, 'adminApp/error.html', {'error_message': 'Username already exists'})
        LabTecnician.objects.create_user(username = username,password = password)
        messages.success(request,f"Account created Succefully {username}")
    
        return redirect('lab-user')
    else:
        return render(request,'adminApp/register.html',{'user':"Lab Technician"})
    
