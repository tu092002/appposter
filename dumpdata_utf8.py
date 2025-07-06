import os
import django

# 👇 Thêm dòng này để Django biết settings nằm ở đâu
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facebook_server.settings")

# 👇 Khởi tạo Django
django.setup()

from django.core.management import call_command
import io

with io.open('data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', indent=2, stdout=f)
