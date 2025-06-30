from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .models import Company
from employees.models import Employee
from attendance.models import Attendance
from django.utils import timezone
from datetime import datetime, timedelta

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def register_company(request):
    if request.method == 'POST':
        # Company details
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        company_phone = request.POST.get('company_phone')
        company_address = request.POST.get('company_address')
        
        # Admin details
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth/register.html')
        
        try:
            with transaction.atomic():
                # Create admin user
                admin_user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                
                # Create company
                company = Company.objects.create(
                    name=company_name,
                    email=company_email,
                    phone=company_phone,
                    address=company_address,
                    admin=admin_user
                )
                
                # Create admin employee
                Employee.objects.create(
                    user=admin_user,
                    company=company,
                    department='IT',
                    role='Admin',
                    joining_date=timezone.now().date()
                )
                
                login(request, admin_user)
                messages.success(request, f'Company {company_name} created successfully!')
                return redirect('dashboard')
                
        except Exception as e:
            messages.error(request, f'Error creating company: {str(e)}')
    
    return render(request, 'auth/register.html')

@login_required
def dashboard(request):
    try:
        employee = Employee.objects.get(user=request.user)
        company = employee.company
        
        # Get today's attendance for current user
        today = timezone.now().date()
        today_attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today
        )
        
        context = {
            'employee': employee,
            'company': company,
            'today_attendance': today_attendance,
        }
        
        # Admin-specific data
        if employee.role == 'Admin':
            # Get all employees in company
            employees = Employee.objects.filter(company=company)
            
            # Get today's attendance for all employees
            today_attendances = Attendance.objects.filter(
                employee__company=company,
                date=today
            )
            
            # Statistics
            total_employees = employees.count()
            checked_in_today = today_attendances.filter(check_in_time__isnull=False).count()
            checked_out_today = today_attendances.filter(check_out_time__isnull=False).count()
            
            # Recent attendance (last 7 days)
            week_ago = today - timedelta(days=7)
            recent_attendances = Attendance.objects.filter(
                employee__company=company,
                date__gte=week_ago
            ).order_by('-date', '-check_in_time')[:20]
            
            context.update({
                'employees': employees,
                'today_attendances': today_attendances,
                'total_employees': total_employees,
                'checked_in_today': checked_in_today,
                'checked_out_today': checked_out_today,
                'recent_attendances': recent_attendances,
            })
        
        return render(request, 'dashboard.html', context)
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('home')
