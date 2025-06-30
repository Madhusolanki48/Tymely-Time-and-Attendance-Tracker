from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
    ]
    
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Team Lead', 'Team Lead'),
        ('Employee', 'Employee'),
        ('Intern', 'Intern'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=2, choices=DEPARTMENT_CHOICES, default='IT')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Employee')
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Generate employee ID
            last_employee = Employee.objects.filter(company=self.company).order_by('id').last()
            if last_employee:
                last_id = int(last_employee.employee_id.split('-')[-1])
                self.employee_id = f"{self.company.name[:3].upper()}-{str(last_id + 1).zfill(3)}"
            else:
                self.employee_id = f"{self.company.name[:3].upper()}-001"
        super().save(*args, **kwargs)
