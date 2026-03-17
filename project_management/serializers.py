from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    project_manager_name = serializers.CharField(
        source="project_manager.full_name",
        read_only=True,
    )
    completion_percentage = serializers.FloatField(read_only=True)
    remaining_budget = serializers.DecimalField(
        read_only=True,
        max_digits=14,
        decimal_places=2,
        allow_null=True,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "code",
            "description",
            "project_manager",
            "project_manager_name",
            "status",
            "priority",
            "start_date",
            "end_date",
            "budget",
            "spent_budget",
            "remaining_budget",
            "github_url",
            "is_active",
            "completion_percentage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "project_manager_name",
            "remaining_budget",
            "completion_percentage",
            "created_at",
            "updated_at",
        ]
