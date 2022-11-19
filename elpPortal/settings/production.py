from elpPortal.settings.base import (
    ALLOWED_HOSTS,
    CORS_ALLOWED_ORIGIN_REGEXES,
    CORS_ALLOWED_ORIGINS,
)

DEBUG = False

ALLOWED_HOSTS += [
    "api-elpPortal.herokuapp.com",
]

CORS_ALLOWED_ORIGINS += [
    "https://elpPortal.netlify.app",
]


CORS_ALLOWED_ORIGIN_REGEXES += [
    r"^https:\/\/*\.elpPortal\.co\.ke",
    r"(^|^[^:]+:\/\/|[^\.]+\.)elpPortal\.co\.ke",
]
