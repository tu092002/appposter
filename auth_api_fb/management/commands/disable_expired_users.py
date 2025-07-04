# auth_api_fb/management/commands/disable_expired_users.py
from django.core.management.base import BaseCommand
from auth_api_fb.models import CustomUser
from datetime import date

class Command(BaseCommand):
    help = "Vô hiệu hóa user đã hết hạn"

    def handle(self, *args, **kwargs):
        expired_users = CustomUser.objects.filter(expiry_date__lt=date.today(), is_active=True)
        count = expired_users.update(is_active=False)
        self.stdout.write(f"✅ Đã disable {count} user hết hạn.")
