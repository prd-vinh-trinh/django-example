from django.urls import path, include
from rest_framework_nested import routers
from api_users.views import UserViewSet

app_name = "users"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path(
        r'api/v1/users/', include(router.urls)
    ),
]
