import re
from typing import Any

from django.core.exceptions import ValidationError


def phone_number_validator(value: str) -> Any:
    """
    Validate phone number.
    """

    if re.match(  # noqa W605 type: ignore["return-value"]
        r"^254[0-9]{9}$", value
    ):
        return value

    raise ValidationError("Invalid phone number")
