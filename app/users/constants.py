USER_GROUPS = ["elp", "wings to fly", "egf", "chapter leader"]


USER_SEARCH_FIELDS = (
    "id",
    "phone_number",
    "first_name",
    "last_name",
)

REGISTRATION_DETAILS_SEARCH_FIELDS = (
    ("id",)
    + tuple(f"user__{search_field}" for search_field in USER_SEARCH_FIELDS)
    + tuple(
        f"registered_by__{search_field}" for search_field in USER_SEARCH_FIELDS
    )
)
