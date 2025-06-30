from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'company', 'department', 'role', 'joining_date', 'is_active')
    list_filter = ('company', 'department', 'role', 'is_active', 'joining_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')
    readonly_fields = ('employee_id', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'company')
