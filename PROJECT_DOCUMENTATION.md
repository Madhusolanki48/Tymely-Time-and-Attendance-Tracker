# Time and Attendance Tracking System

## Project Overview

A comprehensive Django-based time and attendance tracking system with role-based access control, featuring a modern responsive web interface built with HTML, Tailwind CSS, and JavaScript.

## Features

### Core Features
- **Company Management**: Company creation and administration
- **Employee Management**: Employee onboarding, profile management, and role assignment
- **Role-Based Access Control**: Admin, Manager, Team Lead, Employee, and Intern roles
- **Department Support**: HR and IT departments
- **Time Tracking**: Daily check-in/check-out with automatic time calculations
- **Attendance Reports**: Comprehensive reporting system with export capabilities
- **Responsive Design**: Mobile-friendly interface that works on all devices

### System Capabilities
- **Dashboard**: Role-specific dashboards with relevant information
- **Real-time Updates**: Live time tracking and status updates
- **Data Export**: CSV export functionality for reports
- **Password Management**: Admin-controlled password reset functionality
- **Employee Profiles**: Detailed employee information and attendance history

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Python 3.x**: Programming language
- **SQLite**: Database (development)
- **Django REST Framework**: API endpoints

### Frontend
- **HTML5**: Markup language
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icons
- **Responsive Design**: Mobile-first approach

## Project Structure

```
Time and Attendance Tracker/
│
├── attendance_system/          # Main Django project
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── companies/                 # Company management app
│   ├── models.py             # Company model
│   ├── views.py              # Company views
│   ├── urls.py               # Company URLs
│   ├── admin.py              # Admin configuration
│   └── migrations/           # Database migrations
│
├── employees/                 # Employee management app
│   ├── models.py             # Employee model
│   ├── views.py              # Employee views
│   ├── urls.py               # Employee URLs
│   ├── admin.py              # Admin configuration
│   └── migrations/           # Database migrations
│
├── attendance/                # Attendance tracking app
│   ├── models.py             # Attendance model
│   ├── views.py              # Attendance views
│   ├── urls.py               # Attendance URLs
│   ├── admin.py              # Admin configuration
│   └── migrations/           # Database migrations
│
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── home.html             # Landing page
│   ├── dashboard.html        # Main dashboard
│   ├── auth/                 # Authentication templates
│   ├── employees/            # Employee templates
│   └── attendance/           # Attendance templates
│
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Custom CSS
│   └── js/
│       └── app.js            # Custom JavaScript
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
└── db.sqlite3                # SQLite database (created after migrations)
```

## Database Schema

### Company Model
- `id`: Primary key
- `name`: Company name
- `email`: Company email
- `phone`: Company phone (optional)
- `address`: Company address (optional)
- `admin`: Foreign key to User (company admin)
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Employee Model
- `id`: Primary key
- `user`: One-to-one relationship with Django User
- `company`: Foreign key to Company
- `employee_id`: Unique employee identifier (auto-generated)
- `phone`: Employee phone (optional)
- `department`: Choice field (HR, IT)
- `role`: Choice field (Admin, Manager, Team Lead, Employee, Intern)
- `joining_date`: Date field
- `is_active`: Boolean field
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Attendance Model
- `id`: Primary key
- `employee`: Foreign key to Employee
- `date`: Date field
- `check_in_time`: DateTime (optional)
- `check_out_time`: DateTime (optional)
- `total_hours`: Duration field (calculated)
- `notes`: Text field (optional)
- `created_at`: Timestamp
- `updated_at`: Timestamp

## Installation Guide

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd "Time and Attendance Tracker"
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Open browser and go to `http://127.0.0.1:8000`

## Usage Guide

### Getting Started

1. **Company Registration**
   - Visit the home page
   - Click "Register Company"
   - Fill in company and admin details
   - Submit the form to create your company account

2. **Admin Login**
   - Use the email and password created during registration
   - Access the admin dashboard

3. **Adding Employees**
   - Navigate to "Employees" → "Add Employee"
   - Fill in employee details
   - Set department (HR/IT) and role
   - Generate or set password
   - Employee can now log in with their credentials

### Daily Operations

1. **Employee Check-in/Check-out**
   - Employees log in with their credentials
   - Use the dashboard to check in when starting work
   - Check out when finishing work
   - System automatically calculates total hours

2. **Viewing Attendance**
   - Employees can view their attendance in "My Attendance"
   - Admins can view all attendance in the dashboard and reports

3. **Reports and Analytics**
   - Admins can generate attendance reports
   - Filter by date range, department, or employee
   - Export reports to CSV format

### Admin Functions

1. **Employee Management**
   - View all employees
   - Edit employee profiles
   - Reset employee passwords
   - Activate/deactivate employees

2. **Attendance Monitoring**
   - View daily attendance summary
   - Track who's currently working
   - Generate comprehensive reports

## User Roles and Permissions

### Admin
- Full system access
- Company management
- Employee management (add, edit, delete)
- Password reset capabilities
- All attendance reports
- System configuration

### Manager
- Department-level access
- View team attendance
- Basic reporting
- Employee profile viewing

### Team Lead
- Team-level access
- View team member attendance
- Basic reporting

### Employee
- Personal attendance tracking
- Check-in/check-out functionality
- View personal attendance history
- Update personal profile

### Intern
- Basic attendance tracking
- Limited system access
- Personal attendance viewing

## API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /register/` - Company registration

### Attendance
- `POST /attendance/check-in/` - Check in
- `POST /attendance/check-out/` - Check out
- `GET /attendance/today/` - Today's attendance
- `GET /attendance/reports/` - Attendance reports

### Employees
- `GET /employees/list/` - Employee list
- `POST /employees/add/` - Add employee
- `GET /employees/profile/<id>/` - Employee profile
- `PUT /employees/edit/<id>/` - Edit employee
- `POST /employees/reset-password/<id>/` - Reset password

## Customization

### Adding New Departments
1. Update `DEPARTMENT_CHOICES` in `employees/models.py`
2. Run migrations
3. Update templates as needed

### Adding New Roles
1. Update `ROLE_CHOICES` in `employees/models.py`
2. Run migrations
3. Update permission logic in views
4. Update templates as needed

### Styling Customization
- Modify `static/css/style.css` for custom styles
- Update Tailwind classes in templates
- Add new JavaScript functionality in `static/js/app.js`

## Security Features

- CSRF protection on all forms
- Password hashing using Django's built-in system
- Role-based access control
- SQL injection prevention
- XSS protection
- Secure session management

## Performance Considerations

- Database query optimization with select_related and prefetch_related
- Efficient pagination for large datasets
- Static file optimization
- Browser caching for static assets
- Minimal JavaScript libraries for faster loading

## Testing

### Manual Testing Checklist
- [ ] Company registration works
- [ ] Admin login functionality
- [ ] Employee creation and management
- [ ] Check-in/check-out functionality
- [ ] Attendance report generation
- [ ] CSV export functionality
- [ ] Password reset functionality
- [ ] Role-based access control
- [ ] Mobile responsiveness

### Automated Testing
```bash
python manage.py test
```

## Deployment

### Production Settings
1. Update `settings.py` for production
2. Set `DEBUG = False`
3. Configure allowed hosts
4. Set up proper database (PostgreSQL recommended)
5. Configure static files serving
6. Set up SSL/HTTPS
7. Configure backup strategy

### Environment Variables
Create a `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

## Troubleshooting

### Common Issues

1. **Migration Errors**
   - Delete migration files and recreate
   - Check model relationships

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATICFILES_DIRS

3. **Template Not Found**
   - Verify template paths in settings
   - Check template directory structure

4. **Permission Denied**
   - Check user roles and permissions
   - Verify login requirements

## Future Enhancements

- Email notifications for attendance
- Mobile app development
- Advanced reporting with charts
- Integration with HR systems
- Biometric authentication support
- Overtime tracking
- Leave management system
- Multi-language support
- Dark mode theme
- Real-time notifications

## Support

For support or questions:
1. Check the documentation
2. Review troubleshooting section
3. Submit issues on the project repository
4. Contact system administrator

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Changelog

### Version 1.0.0
- Initial release
- Basic time tracking functionality
- Role-based access control
- Responsive web interface
- CSV export capabilities
- Employee management system
