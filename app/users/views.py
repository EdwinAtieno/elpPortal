from typing import Any

from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from rest_framework import (
    exceptions,
    generics,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.permissions import IsAdminChapterLeaderCX
from app.users.permissions import (
    IsChapterLeaderPostOrAdmin,
    IsObjectOwnerOrAdmin,
)
from app.users.serializers import UserSerializer

User = get_user_model()


class UserList(generics.ListCreateAPIView):
    """
    List all users, or create a new user by admin.
    """

    queryset = User.objects.prefetch_related("groups").all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsChapterLeaderPostOrAdmin)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user instance.
    """

    queryset = User.objects.prefetch_related("groups").all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsObjectOwnerOrAdmin,
    )

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        User must authenticate before deleting their account
        """
        user = request.user
        data = request.data
        authenticated_user = authenticate(
            phone_number=user.phone_number, password=data.get("password")  # type: ignore[union-attr]
        )
        if authenticated_user is not None or user.is_superuser:
            return self.destroy(request, *args, **kwargs)

        raise exceptions.AuthenticationFailed({"detail": "Invalid password"})


class ChapterLeaderRetrieveUser(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsAdminChapterLeaderCX)
    queryset = User.objects.prefetch_related("groups").all()
    serializer_class = UserSerializer
    lookup_field = "phone_number"

    def get_queryset(self) -> Any:
        return super().get_queryset().filter(groups__name="elp")
