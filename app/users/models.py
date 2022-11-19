from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.abstracts import (
    IDModel,
    TimeStampedModel,
)
from app.users.validators import phone_number_validator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self, phone_number: str, password: str, **kwargs: Any
    ) -> Any:
        """
        Creates and saves a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError("User must have a phone number")

        if kwargs.get("id_number") == "" or kwargs.get("id_number") is None:
            kwargs.setdefault("id_number", None)

        user = self.model(phone_number=phone_number, **kwargs)
        user.set_password(password)  # type: ignore[attr-defined]
        user.save()
        return user

    def create_user(
        self, phone_number: str, password: str, **kwargs: Any
    ) -> Any:
        kwargs.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **kwargs)

    def create_superuser(
        self, phone_number: str, password: str, **kwargs: Any
    ) -> Any:
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        superuser = self._create_user(phone_number, password, **kwargs)
        group, _ = Group.objects.get_or_create(name="admin")
        superuser.groups.add(group)

        return superuser


class User(AbstractBaseUser, PermissionsMixin, IDModel, TimeStampedModel):
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    middle_name = models.CharField(
        max_length=255, verbose_name=_("Middle Name"), blank=True, null=True
    )
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Phone Number"),
        validators=[
            phone_number_validator,
        ],
    )
    email = models.EmailField(unique=True, max_length=255)
    id_number = models.CharField(
        max_length=255, verbose_name=_("ID Number"), null=True, unique=True
    )
    pf_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Pf Number"),
    )
    scholar_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Scholar Number"),
    )

    alternate_phone_number = models.CharField(
        verbose_name=_("Alternate Phone Number"),
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        validators=[
            phone_number_validator,
        ],
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )

    is_available = models.BooleanField(
        _("available"),
        default=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_phone_numbers",
                fields=["phone_number", "alternate_phone_number"],
            ),
        ]


class RegistrationDetail(models.Model):
    """
    Displays who has registered a new user
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="registered_user",
        verbose_name=_("User"),
    )
    registered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="registered_by",
        verbose_name=_("Registered By"),
    )
    registered_on = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Registered On")
    )

    def __str__(self) -> str:
        return f"{self.user} registered by {self.registered_by}"
