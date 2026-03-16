from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Full department name, e.g. 'Engineering' or 'Finance'."
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Short uppercase code used in reports, e.g. 'ENG' or 'FIN'."
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description of the department's purpose, responsibilities, or scope."
    )
    manager = models.ForeignKey(
        'Employee',
        on_delete = models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_department',
        help_text="The employee who leads this department."
    )
    # is_active = models.BooleanField(
    #     default=True,
    #     help_text="Indicates whether the department is currently active and available for use."
    # )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.code} ({self.name})"

    @property
    def headcount(self):
        return self.employees.filter(status='ACTIVE').count()


class Position(models.Model):
    LEVEL_CHOICES =[
        ('JUNIOR', 'Junior'),
        ('MID','Mid-Level' ),
        ('SENIOR', 'Senior'),
        ('LEAD', 'Lead / Principal'),
        ('MANAGER', 'Manager'),
        ('DIRECTOR', 'Director'),
    ]
    title = models.CharField(
        max_length=150,
        unique=True,
        help_text=" Official job title , e.g. 'Senior Software Engineer'."
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="positions",
        help_text="The department this position belongs to.",
    )

    level = models.CharField(
        max_length=20,
        choices = LEVEL_CHOICES,
        help_text = " Seniority level of this position ."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of duties and expectations."
    )
    min_salary = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        help_text="Minimum gross salary for this position."
    )

    max_salary = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        help_text="Maximum gross monthly salary for this position."
    )
    base_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["department","level","title"]
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self):
        return f"{self.title} {self.level} {self.department.code}"
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.min_salary <= self.base_salary:
            if self.min_salary > self.base_salary:
                raise ValidationError(
                    "Minimum salary cannot exceed maximum salary."
                )

from django.conf import settings
from django.db import models


class Employee(models.Model):
    GENDER_CHOICES = [
        ( "MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
        ('PREFER_NOT_TO_SAY', 'Prefer not to say')
]
    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full_Time'),
        ('PART_TIME', 'Part_Time'),
        ('CONTRACT', 'Contract'),
        ('INTERN', 'Intern'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ON_LEAVE', 'On Leave'),
        ('SUSPENDED', 'Suspended'),
        ('TERMINATED', 'Terminated'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        help_text="System user account linked to this employee profile."
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="Human-readable ID shown on badges , e.g 'EMP-2024-001"
    )
    first_name = models.CharField(
        max_length=50,
        help_text="Employee's legal first name."
    )
    last_name = models.CharField(
        max_length=50,
        help_text="Employee's legal surname."
    )
    email = models.EmailField(
        unique=True,
        help_text="Unique work email address for the employee."
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Primary phone number for contacting the employee."
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="Employee's date of birth."
    )
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        blank=True,
        help_text="Employee's self identified gender."
    )

    national_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        help_text="National ID card or passport number for payroll compliance."
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Residential or mailing address of the employee."
    )
    profile_photo = models.ImageField(
        upload_to="employees/photos/",
        blank=True,
        null=True,
        help_text="Staff profile photo (JPEG or PNG , max 2 MB)."
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
        help_text="Department where the employee is currently assigned."
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
        help_text="Position or job role currently held by the employee."
    )

    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_reports",
        help_text="The employee's direct line manager. Null for top-level staff."
    )

    hire_date = models.DateField(
        help_text="Official date when the employee joined the organization."
    )

    end_date=models.DateField(
        blank=True,
        null=True,
        help_text="Termination date. Null if currently employed."
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='FULL_TIME',
        help_text="The nature of the employment contract."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        help_text="Current employment status of the employee."
    )

    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Current salary amount paid to the employee."
    )

    bank_account = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Bank account for salary disbursement."
    )

    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Full name of the employee's emergency contact person."
    )
    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Phone number of the employee's emergency contact person."
    )

    leave_balance = models.PositiveIntegerField(
        default=21,
        help_text="Number of annual leave days remaining."
                  "Reset to company policy value at start of each year."
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,

    )

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.employee_id} {self.full_name} "

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    @property
    def years_of_service(self):
        from datetime import date
        end = self.end_date or date.today()
        return (end - self.hire_date).days // 365
    def save(self, *args, **kwargs):
        if not self.employee_id:
            from datetime import date
            year = date.today().year
            last = Employee.objects.order_by('-id').first()
            next_num = (last.id + 1) if last else 1
            self.employee_id = f"EMP - {year}-{next_num:04d}"
        super().save(*args, **kwargs)