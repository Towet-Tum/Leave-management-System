from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Employee

class EmployeeAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'department', 'is_supervisor', 'is_staff', 'is_active')
    list_filter = ('is_supervisor', 'is_staff', 'is_active', 'department')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'department', 'joining_date')}),
        (_('Permissions'), {'fields': ('is_supervisor', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'department', 'password1', 'password2', 'is_supervisor', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(Employee, EmployeeAdmin)
