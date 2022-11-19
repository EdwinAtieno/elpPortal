from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.users.constants import USER_GROUPS
from app.users.models import RegistrationDetail
from app.users.validators import phone_number_validator
from app.utils import generate_number

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255)
    middle_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(
        max_length=20,
        validators=[
            phone_number_validator,
            UniqueValidator(
                queryset=User.objects.all(),
                message="This phonenumber already exists",
                lookup="iexact",
            ),
        ],
    )
    email = serializers.EmailField(
        max_length=255,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This email already exists",
                lookup="iexact",
            ),
        ],
    )
    pf_number = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This Pf number already exists",
                lookup="iexact",
            ),
        ],
    )
    scholar_number = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This scholar number already exists",
                lookup="iexact",
            ),
        ],
    )
    alternate_phone_number = serializers.CharField(
        max_length=20,
        required=False,
        validators=[
            phone_number_validator,
        ],
    )
    id_number = serializers.IntegerField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    roles = serializers.SerializerMethodField()
    role = serializers.CharField(max_length=255, write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "phone_number",
            "alternate_phone_number",
            "pf_number",
            "scholar_number",
            "id_number",
            "role",
            "roles",
            "user",
        )
        read_only_fields = ("id", "roles")

    def get_roles(self, obj: Any) -> Any:
        return list(obj.groups.values_list("name", flat=True))

    def validate_phone_number(self, phone_number: Any) -> Any:
        if not User.objects.filter(
            Q(phone_number=phone_number)
            | Q(alternate_phone_number=phone_number)
        ).exists():
            return phone_number

        raise serializers.ValidationError("This phone number already exists")

    def validate_alternate_phone_number(self, phone_number: Any) -> Any:
        if not User.objects.filter(
            Q(phone_number=phone_number)
            | Q(alternate_phone_number=phone_number)
        ).exists():
            return phone_number

        raise serializers.ValidationError("This phone number already exists")

    def validate_role(self, role: Any) -> Any:
        """
        Ensure that the role provided is valid
        """

        user = self.context["request"].user

        if user.groups.filter(name="chapter leader").exists():
            role = "elp"

        role = role.lower()
        if role in USER_GROUPS:
            return role

        raise serializers.ValidationError(
            f"Invalid role. Only {', '.join(USER_GROUPS)} are allowed"
        )

    def validate(self, data: Any) -> Any:
        alternate_phone_number = data.get("alternate_phone_number")
        phone_number = data.get("phone_number")

        if alternate_phone_number and alternate_phone_number == phone_number:
            raise serializers.ValidationError(
                {
                    "alternate_phone_number": "Phone number cannot be same as primary phone number"
                }
            )

        return data

    def create(self, validated_data: Any) -> Any:
        pin = str(generate_number(num_digits=4))

        role = validated_data.pop("role")
        validated_data["password"] = pin
        logged_in_user = validated_data.pop("user")

        user = User.objects.create_user(**validated_data)
        RegistrationDetail.objects.create(
            user=user, registered_by=logged_in_user
        )
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        # send pin using email or sms

        return user
