from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from .models import Employee
from companies.models import Company
from attendance.models import Attendance
from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def add_employee(request):
    try:
        current_employee = Employee.objects.get(user=request.user)
        if current_employee.role != 'Admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Employee details
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        role = request.POST.get('role')
        joining_date = request.POST.get('joining_date')
        password = request.POST.get('password')
        
        # Validation
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'employees/add_employee.html')
        
        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                
                # Create employee
                employee = Employee.objects.create(
                    user=user,
                    company=current_employee.company,
                    phone=phone,
                    department=department,
                    role=role,
                    joining_date=joining_date
                )
                
                messages.success(request, f'Employee {first_name} {last_name} added successfully!')
                return redirect('employee_list')
                
        except Exception as e:
            messages.error(request, f'Error adding employee: {str(e)}')
    
    return render(request, 'employees/add_employee.html')

@login_required
def employee_list(request):
    try:
        current_employee = Employee.objects.get(user=request.user)
        if current_employee.role != 'Admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
        
        employees = Employee.objects.filter(company=current_employee.company).order_by('-created_at')
        
        # Calculate statistics
        total_employees = employees.count()
        hr_employees = employees.filter(department='HR').count()
        it_employees = employees.filter(department='IT').count()
        active_employees = employees.filter(user__is_active=True).count()
        
        context = {
            'employees': employees,
            'total_employees': total_employees,
            'hr_employees': hr_employees,
            'it_employees': it_employees,
            'active_employees': active_employees,
        }
        
        return render(request, 'employees/employee_list.html', context)
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

@login_required
def employee_profile(request, employee_id):
    try:
        current_employee = Employee.objects.get(user=request.user)
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Check if user can view this profile
        if current_employee.role != 'Admin' and current_employee.id != employee.id:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
        
        # Check if employee belongs to same company
        if current_employee.company != employee.company:
            messages.error(request, 'Employee not found.')
            return redirect('dashboard')
        
        # Get attendance records for last 30 days
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        attendances = Attendance.objects.filter(
            employee=employee,
            date__gte=thirty_days_ago
        ).order_by('-date')
        
        # Calculate statistics
        total_days = attendances.count()
        present_days = attendances.filter(check_in_time__isnull=False).count()
        absent_days = 30 - present_days
        
        context = {
            'employee': employee,
            'attendances': attendances,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'current_employee': current_employee,
        }
        
        return render(request, 'employees/employee_profile.html', context)
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

@login_required
def edit_employee(request, employee_id):
    try:
        current_employee = Employee.objects.get(user=request.user)
        if current_employee.role != 'Admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
        
        employee = get_object_or_404(Employee, id=employee_id, company=current_employee.company)
        
        if request.method == 'POST':
            # Update user details
            employee.user.first_name = request.POST.get('first_name')
            employee.user.last_name = request.POST.get('last_name')
            employee.user.email = request.POST.get('email')
            employee.user.username = request.POST.get('email')
            employee.user.save()
            
            # Update employee details
            employee.phone = request.POST.get('phone')
            employee.department = request.POST.get('department')
            employee.role = request.POST.get('role')
            employee.joining_date = request.POST.get('joining_date')
            employee.is_active = request.POST.get('is_active') == 'on'
            employee.save()
            
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_profile', employee_id=employee.id)
        
        return render(request, 'employees/edit_employee.html', {'employee': employee})
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

@login_required
def reset_password(request, employee_id):
    try:
        current_employee = Employee.objects.get(user=request.user)
        if current_employee.role != 'Admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
        
        employee = get_object_or_404(Employee, id=employee_id, company=current_employee.company)
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'employees/reset_password.html', {'employee': employee})
            
            employee.user.set_password(new_password)
            employee.user.save()
            
            messages.success(request, f'Password reset successfully for {employee.user.get_full_name()}!')
            return redirect('employee_profile', employee_id=employee.id)
        
        return render(request, 'employees/reset_password.html', {'employee': employee})
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')
