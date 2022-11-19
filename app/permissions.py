from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminChapterLeaderCX(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name="chapter leader").exists():  # type: ignore[union-attr]
            return True

        if request.user.groups.filter(name="egf").exists():  # type: ignore[union-attr]
            return True

        return False
