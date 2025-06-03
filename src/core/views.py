from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.db.models import Count
from datetime import timedelta
from config.permission import DoctorPermissionMixin, DoctorNursePermissionMixin

from src.core.models import Patient, PatientMedication, MedicationLog, Medication
from src.core.forms import PatientForm, PatientMedicationForm, MedicationLogForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["number_of_patients"] = Patient.objects.all().count()
        ctx["total_medication"] = Medication.objects.all().count()
        ctx["total_logs"] = MedicationLog.objects.filter(
            log_datetime__date=timezone.now().date()
        ).count()
        daily_medication_to_log = PatientMedication.objects.all().count()
        ctx["daily_medication_to_log"] = daily_medication_to_log
        ctx["daily_prescribed_patient"] = PatientMedication.objects.filter(
            prescription_date=timezone.now().date()
        ).count()
        ctx["gender_count"] = Patient.objects.values("gender").annotate(
            total=Count("id")
        )
        expiring = Medication.objects.filter(
            expiry_date__lte=timezone.now().date() + timedelta(days=7)
        ).count()
        ctx["expiring_in_7_days"] = expiring
        return ctx


class PatientListRetrieveView(DoctorNursePermissionMixin, ListView):
    template_name = "patient_list.html"
    model = Patient
    context_object_name = "patients"
    form_class = PatientMedicationForm

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs.get("pk"))

    def get_template_names(self):
        if self.kwargs.get("pk"):
            return ["patient_detail.html"]
        return super().get_template_names()

    def post(self, request, *args, **kwargs):
        if self.kwargs.get("pk") and request.user.groups.filter(name="Doctor").exists():
            data = request.POST
            form = self.form_class(data)
            if form.is_valid():
                form.save(commit=False)
                form.instance.patient = self.get_object()
                form.save()
                messages.success(request, "Medication added successfully")
            else:
                print(form.errors)
                messages.error(request, "Medication added failed")
        return redirect("patient_detail", pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        if self.kwargs.get("pk"):
            instance = self.get_object()
            kwargs["instance"] = instance
            medications = PatientMedication.objects.filter(patient=instance)
            kwargs["medications"] = medications
            kwargs["form"] = self.form_class()
            logs = MedicationLog.objects.filter(patient_medication__patient=instance)
            kwargs["logs"] = logs
            kwargs["log_form"] = MedicationLogForm()
        return super().get_context_data(**kwargs)


class PatientCreateUpdateView(DoctorPermissionMixin, ListView):
    template_name = "patient_create.html"
    model = Patient
    form_class = PatientForm
    context_object_name = "patients"

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs.get("pk"))

    def post(self, request, *args, **kwargs):
        if self.kwargs.get("pk"):
            instance = self.get_object()
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            instance = form.save()
            messages.success(request, "Patient updated successfully")
            return redirect("patient_update", pk=instance.id)
        else:
            messages.error(request, "Patient updated failed")
            form = self.form_class(request.POST)
        return render(request, self.template_name, {"form": form})

    def get_context_data(self, **kwargs):
        if self.kwargs.get("pk"):
            instance = self.get_object()
            kwargs["instance"] = instance
            kwargs["form"] = self.form_class(instance=instance)
        else:
            kwargs["form"] = self.form_class()
        return super().get_context_data(**kwargs)


@login_required
def log_patient_medication(request, pk):
    if request.method == "POST":
        form = MedicationLogForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.patient_medication = PatientMedication.objects.get(pk=pk)
            form.save()
            messages.success(request, "Medication logged successfully")
        else:
            messages.error(request, "Medication logged failed")
    return redirect("patient_detail", pk=pk)


@login_required
def delete_patient_medication(request, pk):
    medication = PatientMedication.objects.get(pk=pk)
    medication.delete()
    messages.success(request, "Medication deleted successfully")
    return redirect("patient_detail", pk=medication.patient.id)
