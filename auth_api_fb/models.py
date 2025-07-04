from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, date

# class CustomUser(AbstractUser):
#     expiry_date = models.DateField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)  # override
class CustomUser(AbstractUser):
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = date.today() + timedelta(days=365)  # Hết hạn sau 1 năm
        super().save(*args, **kwargs)