# decorators.py

from functools import wraps
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.role == 'ADMIN'

def is_receptionist(user):
    return user.role == 'RECEPTION'

def is_nurse(user):
    return user.role == 'NURSE'

def is_doctor(user):
    return user.role == 'DOCTOR'

def is_lab_technician(user):
    return user.role == 'LABIST'

def is_radiologist(user):
    return user.role == 'RADIOLOGITS'

admin_required = user_passes_test(is_admin)
receptionist_required = user_passes_test(is_receptionist)
nurse_required = user_passes_test(is_nurse)
doctor_required = user_passes_test(is_doctor)
lab_technician_required = user_passes_test(is_lab_technician)
radiologist_required = user_passes_test(is_radiologist)
