from rest_framework import serializers

from .models import LeaveType, LeaveRequest


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = [
            "id",
            "name",
            "code",
            "max_days_per_year",
            "requires_approval",
            "is_paid",
            "description",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source="employee.full_name",
        read_only=True
    )
    leave_type_name = serializers.CharField(
        source="leave_type.name",
        read_only=True
    )
    leave_type_code = serializers.CharField(
        source="leave_type.code",
        read_only=True
    )
    reviewed_by_name = serializers.CharField(
        source="reviewed_by.full_name",
        read_only=True
    )

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "leave_type_name",
            "leave_type_code",
            "start_date",
            "end_date",
            "total_days",
            "reason",
            "status",
            "reviewed_by",
            "reviewed_by_name",
            "reviewed_at",
            "review_comment",
            "attachment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee",
            "employee_name",
            "total_days",
            "status",
            "reviewed_by",
            "reviewed_by_name",
            "reviewed_at",
            "review_comment",
            "created_at",
            "updated_at",
        ]

    def validate_leave_type(self, value):
        if not value.is_active:
            raise serializers.ValidationError("You can only request an active leave type.")
        return value

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": "End date must be greater than or equal to start date."
            })

        return attrs