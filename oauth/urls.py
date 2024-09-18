from django.urls import path, include,re_path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from .views import Oauth2ViewSet

app_name = "oauth"
router = routers.DefaultRouter()

router.register(r"", Oauth2ViewSet, basename="oauth")

urlpatterns = [
    path('api/v1/oauth/', include(router.urls)), 
]
