from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.contrib import messages

from config.permission import DoctorPermissionMixin, DoctorNursePermissionMixin

from src.core.models import Patient, PatientMedication, MedicationLog
from src.core.forms import PatientForm, PatientMedicationForm, MedicationLogForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"


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
