from django.db import models
from django.utils import timezone
from employees.models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    total_hours = models.DurationField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.date}"

    def save(self, *args, **kwargs):
        if self.check_in_time and self.check_out_time:
            self.total_hours = self.check_out_time - self.check_in_time
        super().save(*args, **kwargs)

    @property
    def is_checked_in(self):
        return self.check_in_time is not None and self.check_out_time is None

    @property
    def is_checked_out(self):
        return self.check_in_time is not None and self.check_out_time is not None
