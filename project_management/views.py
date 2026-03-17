from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().select_related("project_manager")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "priority", "is_active", "project_manager"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["start_date", "end_date", "created_at", "updated_at"]
    ordering = ["-start_date", "name"]
