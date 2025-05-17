from django.urls import path
from .views import PatientCreateUpdateView, PatientListRetrieveView, DashboardView, log_patient_medication

urlpatterns = [
    path("patients/", PatientListRetrieveView.as_view(), name="patient_list"),
    path("patients/<int:pk>/", PatientListRetrieveView.as_view(), name="patient_detail"),
    path("patients/<int:pk>/", PatientCreateUpdateView.as_view(), name="patient_update"),
    path("patients/create/", PatientCreateUpdateView.as_view(), name="patient_create"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("patients/<int:pk>/log/", log_patient_medication, name="log_patient_medication"),
]
