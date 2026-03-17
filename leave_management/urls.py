from rest_framework.routers import DefaultRouter

from .views import LeaveRequestViewSet

app_name = "leave_management"

router = DefaultRouter()
router.register("leaves", LeaveRequestViewSet, basename="leave")

urlpatterns = router.urls
