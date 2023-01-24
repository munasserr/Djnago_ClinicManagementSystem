from django import forms
from .models import *

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['notes', 'name', 'address', 'age', 'email', 'phone', 'sex', 'bloodgroup']

class ResrevForm(forms.ModelForm):
    class Meta :
        model = Appointment
        fields = [
            'patient',
            'date',
            'time',
            'notes'
        ]

class BillForm(forms.ModelForm) :
    class Meta:
        model = Bill
        fields = [
            'appointment',
            'amount',
            'notes'
        ]
