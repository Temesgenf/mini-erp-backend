from rest_framework import serializers
from .models import Department, Position, Employee

class DepartmentSerializer(serializers.ModelSerializer):
    headcount = serializers.ReadOnlyField()
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'manager', 'headcount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PositionSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )
    class Meta:
        model = Position
        fields = ['id','title', 'department', 'department_name', 'level', 'min_salary', 'max_salary','description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
    def vaidate(self, attrs):
        if attrs.get('min_salary') and attrs.get('max_salary'):
            if attrs.get['min_salary'] > attrs.get['max_salary']:
                raise serializers.ValidationError('Minimum Salary cannot be greater than maximum salary')
        return attrs

class EmployeeListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='department.full_name')
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )

    position_title = serializers.CharField(
        source='position.title',
        read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'full_name',
            'email', 'department_name', 'position_title',
            'employment_type', 'status', 'hire_date'
        ]

class EmployeeDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='department.full_name')
    years_of_service = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = '__all__ '
        read_only_fields = [
            'id ', 'employee_id ', 'created_at ', 'updated_at ',
             'full_name ', ' years_of_service '

            ]
    def validate(self, value):
        qs = Employee.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('This employee already exists')
        return value
