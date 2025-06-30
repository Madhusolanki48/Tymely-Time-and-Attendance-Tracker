# Time and Attendance Tracking System

A comprehensive Django-based time and attendance tracking system with role-based access control.

## Features

- Company creation and management
- Employee onboarding and management
- Role-based access (Admin, Manager, Team Lead, Employee, Intern)
- Department support (HR, IT)
- Daily check-in/check-out tracking
- Admin dashboard with attendance reports
- Employee profile management

## Setup Instructions

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

## Project Structure

- `attendance_system/` - Main Django project
- `companies/` - Company management app
- `employees/` - Employee management app
- `attendance/` - Attendance tracking app
- `templates/` - HTML templates
- `static/` - CSS, JS, and other static files

## Default Credentials

After setup, create a company admin account through the registration page.
