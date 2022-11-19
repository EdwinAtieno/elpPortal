from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsObjectOwnerOrAdmin(BasePermission):
    """
    Only grant permission to resource if one is owner or admin
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return True

    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> bool:
        if obj == request.user or request.user.is_superuser:
            return True

        return False


class IsChapterLeaderPostOrAdmin(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_superuser:
            return True

        if request.method == "POST" and request.user.groups.filter(name="chapter leader").exists():  # type: ignore[union-attr]
            return True

        return False
