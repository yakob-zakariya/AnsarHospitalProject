from django.urls import path
from .views import PaymentDataAPIView,ZonePatientCountAPI
from .import views

urlpatterns = [
    path('payments',PaymentDataAPIView.as_view(),name='payments'),
    path('zone-patient-count/', ZonePatientCountAPI.as_view(), name='zone-patient-count'),
    
    
    path('patient-list-api/',views.patient_list,name='patient-list-api'),
    path('region/',views.regionView,name='region'),
    path('zones_by_region/<int:region_id>/', views.zones_by_region, name='zones-by-region'),
    path('woredas_by_zone/<int:zone_id>/', views.woredas_by_zone, name='woredas-by-zone'),
    
    
    path('patient/<int:patient_id>/', views.get_patient_details, name='patient_details'),
    
    
    path('user-percentage/', views.UserPercentageView.as_view(), name='user_percentage'),
     
]
