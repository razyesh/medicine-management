from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User.objects.create_superuser(username="admin", password="admin", email="admin@admin.com")
        Group.objects.get_or_create(name="Doctor")
        Group.objects.get_or_create(name="Nurse")
        