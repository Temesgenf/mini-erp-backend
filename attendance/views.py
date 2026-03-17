from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for attendance records.

    GET    /api/attendance/         list
    POST   /api/attendance/         create
    GET    /api/attendance/{id}/    retrieve
    PUT    /api/attendance/{id}/    update
    PATCH  /api/attendance/{id}/    partial update
    DELETE /api/attendance/{id}/    delete
    """

    queryset = AttendanceRecord.objects.all().select_related("employee")
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["employee", "date", "status", "location"]
    search_fields = ["employee__first_name", "employee__last_name", "employee__email"]
    ordering_fields = ["date", "created_at", "updated_at"]
    ordering = ["-date"]
