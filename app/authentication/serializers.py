from typing import Any

from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.core.validators import RegexValidator
from rest_framework import (
    exceptions,
    serializers,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.utils import generate_number

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # type: ignore
    @classmethod
    def get_token(cls, user: Any) -> Any:
        token = super().get_token(user)
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["middle_name"] = user.middle_name
        token["phone_number"] = user.phone_number
        token["pf_number"] = user.pf_number
        token["scholar_number"] = user.scholar_number
        token["roles"] = list(user.groups.values_list("name", flat=True))

        return token


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(max_length=6, write_only=True)
    password = serializers.CharField(max_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=6, write_only=True)

    class Meta:
        model = User
        fields = ("current_password", "password", "confirm_password")

    def validate(self, data: Any) -> Any:
        try:
            int(data["password"])
        except ValueError:
            raise exceptions.ValidationError(
                {"password": "Password must be a number"}
            )

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"detail": "Password must match confirm password"}
            )

        user = self.context["request"].user

        if not authenticate(
            phone_number=user.phone_number,
            password=data["current_password"],
        ):
            raise exceptions.AuthenticationFailed("Invalid password")

        return data

    def update(self, instance: Any, validated_data: Any) -> Any:
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ForgotPasswordSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                # regex to validate phone number is Kenyan
                regex="^(254|0)[1-9]\d{8}$",  # noqa W605
                message="Invalid phonenumber",
            ),
        ],
    )

    class Meta:
        model = User
        fields = ("phone_number",)

    def save(self, **kwargs: Any) -> Any:
        user = User.objects.filter(
            phone_number=self.validated_data.get("phone_number")
        )
        if user.exists():
            pin = str(generate_number(num_digits=4))
            user = user.first()  # type: ignore[assignment]
            user.set_password(str(pin))  # type: ignore[attr-defined]
            user.save()  # type: ignore[attr-defined]

            # send user password/pin

        return user
