from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = list(getattr(UserAdmin, "fieldsets", []) or []) + [
        ("Profile", {"fields": ("bio", "avatar", "created_at", "updated_at")}),
    ]

    add_fieldsets = list(getattr(UserAdmin, "add_fieldsets", []) or []) + [
        ("Profile", {"fields": ("email", "bio", "avatar")}),
    ]

    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
