from django.urls import path
from . import views

urlpatterns = [
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    path('today/', views.today_attendance, name='today_attendance'),
    path('reports/', views.attendance_reports, name='attendance_reports'),
    path('employee-reports/<int:employee_id>/', views.employee_attendance_reports, name='employee_attendance_reports'),
]
