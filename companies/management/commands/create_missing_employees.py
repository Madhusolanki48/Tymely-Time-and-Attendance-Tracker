from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from companies.models import Company
from employees.models import Employee
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create Employee records for company admins that might be missing them'

    def handle(self, *args, **options):
        # Find companies where the admin user doesn't have an employee record
        companies = Company.objects.all()
        created_count = 0
        
        for company in companies:
            admin_user = company.admin
            
            # Check if admin user has an employee record
            if not hasattr(admin_user, 'employee'):
                try:
                    # Create employee record for admin
                    Employee.objects.create(
                        user=admin_user,
                        company=company,
                        department='IT',
                        role='Admin',
                        joining_date=timezone.now().date()
                    )
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created Employee record for admin: {admin_user.get_full_name()} ({admin_user.email})'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error creating Employee record for {admin_user.email}: {str(e)}'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} Employee records.')
        )
