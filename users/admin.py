from django.contrib import admin
from .models import Reception,Nurse,Doctor,LabTecnician,Radiologist
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):
    pass



admin.site.register(Reception,MyUserAdmin)
admin.site.register(Nurse,MyUserAdmin)
admin.site.register(Doctor,MyUserAdmin)
admin.site.register(LabTecnician,MyUserAdmin)
admin.site.register(Radiologist,MyUserAdmin)

# class NurseRegister(admin.ModelAdmin):
#     fields = ('username','email','password',)

# class DoctorRegister(admin.ModelAdmin):
#     fields = ('username','email','password',)



