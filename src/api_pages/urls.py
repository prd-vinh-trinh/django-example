from django.urls import path, include, re_path
from rest_framework_nested import routers
from api_pages.views.page import PageViewSet

app_name = "page"

router = routers.SimpleRouter(trailing_slash=False)

router.register(r"", PageViewSet, basename="page")

urlpatterns = [
    path('api/v1/pages/', include(router.urls)),
]
