from django.urls import path
from .import views

app_name = "tests"

urlpatterns = [
    
    path('order-lab/<int:pk>/',views.fill_lab_test_order,name="order-lab"),
    path('pending/',views.pending_patients,name='pending'),
    path('patient-detail/<int:pk>/',views.patient_detail,name='patient-detail'),
    path('pay-lab/<int:pk>/',views.payLab,name='pay-lab'),
    path('paid-orders/<int:pk>/',views.paid_orders,name='paid-orders'),
    path('pending-lab/',views.pending_lab,name='pending-lab'),
    path('result/<int:pk>/',views.fill_lab_result,name='lab-result'),
    path('patient-history/<int:pk>/',views.patient_history,name='patient-history'),
    path('patient-dr/',views.all_patient_dr,name='patient-dr'),
    path('generate-bar-code/<int:pk>/',views.generateQrCode,name='generate-bar-code'),
]
