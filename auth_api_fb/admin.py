# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# admin.site.register(CustomUser, UserAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin thêm', {'fields': ('expiry_date',)}),
    )
    list_display = ['username', 'email', 'is_active', 'expiry_date']
    list_filter = ['is_active', 'expiry_date']

admin.site.register(CustomUser, CustomUserAdmin)
