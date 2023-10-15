from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='admin-home'),
    path('add-reception/',views.add_reception,name='add-reception'),
    path('reception-user/',views.reception,name='reception-user'),
    path('add-doctor/',views.add_doctor,name='add-doctor'),
    path('doctor-user/',views.doctor,name='doctor-user'),
    path('add-lab/',views.add_lab,name='add-lab'),
    path('lab-user/',views.lab,name='lab-user'),
   
   
]
