from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from rest_framework_nested import routers

from api_auth.views.auth import AuthViewSet

app_name = "auth"

router = routers.SimpleRouter(trailing_slash=False)

router.register(r"", AuthViewSet, basename="auth")

urlpatterns = [
    path('api/v1/auth/', include(router.urls)),
    #     path('api/v1/auth/token/', TokenObtainPairView.as_view(), name="auth-token"),
    path('api/v1/auth/token/refresh/',
         TokenRefreshView.as_view(), name="auth-token-refresh"),
    path('api/v1/auth/token/verify/',
         TokenVerifyView.as_view(), name="auth-token-verify"),
]
