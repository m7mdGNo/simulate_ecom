from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number","country")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
        ("Important Dates", {"fields": ("RegistrationDate",)}),
        ("Image", {"fields": ("image",)}),
        
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("RegistrationDate",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
