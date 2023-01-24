from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(UserCustom)
class UserCustomAdmin(UserAdmin):
   model = UserCustom
   fieldsets = (       
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','first_name', 'last_name','last_login', 'status')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                    'is_active', 'groups',
                                    'user_permissions')}),
    )
   add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'username',
                    'password1', 'password2', 'status')}
        ),
    )


admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Bill)