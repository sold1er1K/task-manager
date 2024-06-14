from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Task


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'password', 'last_name', 'first_name', 'father_name', 'phone', 'email', 'role', 'full_access')
    list_filter = ('role', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'father_name', 'email', 'phone', 'role', 'full_access')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'father_name', 'email', 'phone', 'full_access')}),
        ('Permissions', {'fields': ['role', ]}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Task)
