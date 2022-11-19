from django.urls import path

from app.users.views import (
    ChapterLeaderRetrieveUser,
    UserDetail,
    UserList,
)

urlpatterns = [
    path(
        "users/",
        UserList.as_view(),
        name="users-list",
    ),
    path("users/<str:pk>/", UserDetail.as_view(), name="users-detail"),
    path(
        "users/customers/<str:phone_number>/",
        ChapterLeaderRetrieveUser.as_view(),
        name="agent-retrieve-customer",
    ),
]
