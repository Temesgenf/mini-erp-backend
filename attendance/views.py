from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hr.models import Employee
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

    @action(detail=False, methods=["post"], url_path="check-in")
    def check_in(self, request):
        try:
            employee = request.user.employee_profile
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Authenticated user has no employee profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = timezone.localdate()
        record, created = AttendanceRecord.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                "check_in": timezone.now(),
                "ip_address": request.META.get("REMOTE_ADDR"),
            },
        )

        if not created:
            if record.check_in:
                return Response(
                    {"detail": "You have already checked in today."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            record.check_in = timezone.now()
            if not record.ip_address:
                record.ip_address = request.META.get("REMOTE_ADDR")
            record.save()

        serializer = self.get_serializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="check-out")
    def check_out(self, request):
        try:
            employee = request.user.employee_profile
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Authenticated user has no employee profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = timezone.localdate()
        record = AttendanceRecord.objects.filter(
            employee=employee,
            date=today,
        ).first()

        if not record or not record.check_in:
            return Response(
                {"detail": "No check-in found for today."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if record.check_out:
            return Response(
                {"detail": "You have already checked out today."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        record.check_out = timezone.now()
        record.save()
        serializer = self.get_serializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
