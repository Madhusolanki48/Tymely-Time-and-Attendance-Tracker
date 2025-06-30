from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in_time', 'check_out_time', 'total_hours')
    list_filter = ('date', 'employee__company', 'employee__department')
    search_fields = ('employee__user__username', 'employee__user__first_name', 'employee__user__last_name')
    readonly_fields = ('total_hours', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee', 'employee__user', 'employee__company')
