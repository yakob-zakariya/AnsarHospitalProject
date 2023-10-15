from django import forms
from .models import LabTestResult,LabTest
 
#  the form will return checkbox for every labtest in the database
class LabTestOrderForm(forms.Form):
    lab_tests = forms.ModelMultipleChoiceField(
        queryset=LabTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Select Lab Tests',
    )

class LabTestResultForm(forms.Form):
    class Meta:
        model = LabTestResult
        fields = ['result','result_comment']