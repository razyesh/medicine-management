from django.contrib.auth.mixins import LoginRequiredMixin

class DoctorPermissionMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Doctor").exists():
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class NursePermissionMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Nurse").exists():
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
    


class DoctorNursePermissionMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Doctor").exists() or request.user.groups.filter(name="Nurse").exists():
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()