
from django.db import models
from config.models import TimeStampModel


class Patient(TimeStampModel):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    patient_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    
    def __str__(self):
        return self.name
    

class Medication(TimeStampModel):
    medication_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    mf_date = models.DateField()
    expiry_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    side_effects = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class PatientMedication(TimeStampModel):
    prescription_date = models.DateField(blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage_per_day = models.CharField(max_length=100)


class MedicationLog(TimeStampModel):
    patient_medication = models.ForeignKey(PatientMedication, on_delete=models.CASCADE)
    log_datetime = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    
    