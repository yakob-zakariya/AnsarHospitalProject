from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    # home pages
    path('reception/',views.reception,name='reception'),
    path('nurse/',views.nurse_home,name='nurse-home'),
    path('doctor/',views.doctor_home,name='doctor-home'),
    path('lab-tech/',views.lab_tech_home,name='lab-tech'),
    
    # patients and appointments
    path('register-patient/',views.register_patient,name='patient-register'),
    path('add-appointment',views.add_appointment,name='add-appointment'),
    path('patients/',views.all_patient,name= 'patients'),
    path('appointments/',views.all_appointment,name='appointments'),
    path('update-patient/<int:pk>/',views.update_patient,name='update-patient'),
    path('delete-patient/<int:pk>/',views.delete_patient,name='delete-patient'),
    
    # appointments for doctor (active and all)
    path('doctor-appointment/',views.docotr_appointment,name='doctor-appointment'),
    path('doctor-active-appointment/',views.docotr_active_appointment,name = 'doctor-active-appointment'),
    # login and logout
    path('',CustomLoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name = 'users/logout.html'),name='logout'),

]
