from django.urls import path, include, re_path
from rest_framework_nested import routers
from api_tasks.views.task import TaskViewSet

app_name = "task"

router = routers.SimpleRouter(trailing_slash=False)

router.register(r"", TaskViewSet, basename="page")


urlpatterns = [
    path('api/v1/tasks/', include(router.urls)),
]
