"""
Django admin customization.
"""
from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    model = User
    list_display = ['email', 'is_active', 'is_staff', 'is_superuser']
    ordering = ['-id']
    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),
    )


admin.site.register(User, UserAdmin)
