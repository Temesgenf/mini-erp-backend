from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet

app_name = "project_management"

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")

urlpatterns = router.urls
