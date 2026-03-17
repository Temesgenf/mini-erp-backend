from rest_framework.routers import DefaultRouter

from .views import AttendanceRecordViewSet

app_name = "attendance"

router = DefaultRouter()
router.register("attendance", AttendanceRecordViewSet, basename="attendance")

urlpatterns = router.urls
