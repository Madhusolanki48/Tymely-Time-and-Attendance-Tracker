from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import Attendance
from employees.models import Employee
from datetime import datetime, timedelta
import json

@login_required
def check_in(request):
    try:
        employee = Employee.objects.get(user=request.user)
        today = timezone.now().date()
        
        # Get or create today's attendance record
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today
        )
        
        if attendance.check_in_time:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Already checked in today'}, status=400)
            messages.error(request, 'You have already checked in today.')
            return redirect('dashboard')
        
        # Record check-in time
        attendance.check_in_time = timezone.now()
        attendance.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Checked in successfully!',
                'check_in_time': attendance.check_in_time.strftime('%I:%M %p')
            })
        
        messages.success(request, 'Checked in successfully!')
        return redirect('dashboard')
        
    except Employee.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Employee profile not found'}, status=404)
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

@login_required
def check_out(request):
    try:
        employee = Employee.objects.get(user=request.user)
        today = timezone.now().date()
        
        # Get today's attendance record
        try:
            attendance = Attendance.objects.get(employee=employee, date=today)
        except Attendance.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'No check-in record found for today'}, status=400)
            messages.error(request, 'No check-in record found for today.')
            return redirect('dashboard')
        
        if not attendance.check_in_time:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Please check in first'}, status=400)
            messages.error(request, 'Please check in first.')
            return redirect('dashboard')
        
        if attendance.check_out_time:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Already checked out today'}, status=400)
            messages.error(request, 'You have already checked out today.')
            return redirect('dashboard')
        
        # Record check-out time
        attendance.check_out_time = timezone.now()
        attendance.save()
        
        # Calculate total hours
        total_hours = attendance.check_out_time - attendance.check_in_time
        hours = int(total_hours.total_seconds() // 3600)
        minutes = int((total_hours.total_seconds() % 3600) // 60)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Checked out successfully!',
                'check_out_time': attendance.check_out_time.strftime('%I:%M %p'),
                'total_hours': f'{hours}h {minutes}m'
            })
        
        messages.success(request, f'Checked out successfully! Total time: {hours}h {minutes}m')
        return redirect('dashboard')
        
    except Employee.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Employee profile not found'}, status=404)
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

@login_required
def today_attendance(request):
    try:
        employee = Employee.objects.get(user=request.user)
        today = timezone.now().date()
        
        try:
            attendance = Attendance.objects.get(employee=employee, date=today)
        except Attendance.DoesNotExist:
            attendance = None
        
        context = {
            'attendance': attendance,
            'employee': employee,
            'today': today,
        }
        
        return render(request, 'attendance/today_attendance.html', context)
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

@login_required
def attendance_reports(request):
    try:
        current_employee = Employee.objects.get(user=request.user)
        if current_employee.role != 'Admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
        
        # Get filter parameters
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        department = request.GET.get('department')
        employee_id = request.GET.get('employee_id')
        
        # Build query
        attendances = Attendance.objects.filter(employee__company=current_employee.company)
        
        if date_from:
            attendances = attendances.filter(date__gte=date_from)
        if date_to:
            attendances = attendances.filter(date__lte=date_to)
        if department:
            attendances = attendances.filter(employee__department=department)
        if employee_id:
            attendances = attendances.filter(employee_id=employee_id)
        
        attendances = attendances.order_by('-date', '-check_in_time')
        
        # Get employees for filter dropdown
        employees = Employee.objects.filter(company=current_employee.company)
        
        context = {
            'attendances': attendances,
            'employees': employees,
            'current_employee': current_employee,
            'filters': {
                'date_from': date_from,
                'date_to': date_to,
                'department': department,
                'employee_id': employee_id,
            }
        }
        
        return render(request, 'attendance/reports.html', context)
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

@login_required
def employee_attendance_reports(request, employee_id):
    try:
        current_employee = Employee.objects.get(user=request.user)
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Check access permissions
        if current_employee.role != 'Admin' and current_employee.id != employee.id:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
        
        # Check if employee belongs to same company
        if current_employee.company != employee.company:
            messages.error(request, 'Employee not found.')
            return redirect('dashboard')
        
        # Get date range (default last 30 days)
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        if not date_from:
            date_from = (timezone.now().date() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not date_to:
            date_to = timezone.now().date().strftime('%Y-%m-%d')
        
        attendances = Attendance.objects.filter(
            employee=employee,
            date__gte=date_from,
            date__lte=date_to
        ).order_by('-date')
        
        # Calculate statistics
        total_days = attendances.count()
        present_days = attendances.filter(check_in_time__isnull=False).count()
        
        # Calculate total working hours
        total_seconds = 0
        for attendance in attendances:
            if attendance.total_hours:
                total_seconds += attendance.total_hours.total_seconds()
        
        total_hours = int(total_seconds // 3600)
        total_minutes = int((total_seconds % 3600) // 60)
        
        context = {
            'employee': employee,
            'attendances': attendances,
            'current_employee': current_employee,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': max(0, 30 - present_days),
            'total_working_hours': f'{total_hours}h {total_minutes}m',
            'filters': {
                'date_from': date_from,
                'date_to': date_to,
            }
        }
        
        return render(request, 'attendance/employee_reports.html', context)
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')
