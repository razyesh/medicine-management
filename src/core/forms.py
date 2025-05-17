from django import forms
from django.utils import timezone
from src.core.models import Patient, PatientMedication, MedicationLog


class PatientForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Patient
        fields = [
            "patient_id",
            "name",
            "dob",
            "gender",
            "phone",
            "address",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class PatientMedicationForm(forms.ModelForm):
    prescription_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'value': timezone.now().date()}))

    class Meta:
        model = PatientMedication
        fields = [
            "medication",
            "prescription_date",
            "dosage_per_day",
        ]


    def __init__(self, *args, **kwargs):
        super(PatientMedicationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    


class MedicationLogForm(forms.ModelForm):
    log_datetime = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'), initial=timezone.now, input_formats=['%Y-%m-%dT%H:%M'], )


    class Meta:
        model = MedicationLog
        fields = [
            "log_datetime",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super(MedicationLogForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'