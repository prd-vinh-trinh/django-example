from rest_framework.routers import DefaultRouter
from .views import TestAPIView

router = DefaultRouter()
router.register("/test-api", TestAPIView, basename="task_list")


urlpatterns = []

urlpatterns += router.urls