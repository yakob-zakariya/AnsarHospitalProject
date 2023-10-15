from django.forms import ModelForm
from users.models import Nurse


class NurseRegisterForm(ModelForm):
    class Meta:
        model = Nurse
        fields = '__all__'