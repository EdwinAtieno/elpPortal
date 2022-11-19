from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from app.users.constants import (
    REGISTRATION_DETAILS_SEARCH_FIELDS,
    USER_SEARCH_FIELDS,
)

from .models import RegistrationDetail

User = get_user_model()


class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = (
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "pf_number",
        "scholar_number",
        "id_number",
        "phone_number",
        "alternate_phone_number",
        "created_at",
        "is_superuser",
    )
    list_display_links = (
        "id",
        "phone_number",
    )
    readonly_fields = ("created_at", "updated_at")
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )
    ordering = ("first_name", "last_name")
    search_fields = USER_SEARCH_FIELDS
    exclude = ("username", "email", "date_joined")

    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "pf_number",
                    "scholar_number",
                    "last_name",
                    "id_number",
                    "password",
                )
            },
        ),
        (
            "Contact info",
            {"fields": ("phone_number", "alternate_phone_number")},
        ),
        ("Important dates", {"fields": ("last_login",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            "Personal info",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "pf_number",
                    "scholar_number",
                    "middle_name",
                    "id_number",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Contact info",
            {"fields": ("phone_number", "alternate_phone_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
    )


admin.site.register(User, UserAdmin)


class RegistrationDetailAdmin(admin.ModelAdmin):
    model = RegistrationDetail

    list_display = (
        "id",
        "user_phone_number",
        "user_name",
        "registered_by_phone_number",
        "registered_by_name",
        "registered_on",
    )

    ordering = (
        "registered_on",
        "user__phone_number",
        "registered_by__phone_number",
    )
    search_fields = REGISTRATION_DETAILS_SEARCH_FIELDS

    def user_phone_number(self, obj: RegistrationDetail) -> str:
        try:
            return obj.user.phone_number

        except Exception:
            return ""

    def registered_by_phone_number(self, obj: RegistrationDetail) -> str:
        try:
            return obj.registered_by.phone_number  # type: ignore

        except Exception:
            return ""

    def user_name(self, obj: RegistrationDetail) -> str:
        try:
            return f"{obj.user.first_name or ''} {obj.user.middle_name or ''} {obj.user.last_name or ''}"

        except Exception:
            return ""

    def registered_by_name(self, obj: RegistrationDetail) -> str:
        try:
            return f"{obj.registered_by.first_name or ''} {obj.registered_by.middle_name or ''} {obj.registered_by.last_name or ''}"  # type: ignore

        except Exception:
            return ""


admin.site.register(RegistrationDetail, RegistrationDetailAdmin)
