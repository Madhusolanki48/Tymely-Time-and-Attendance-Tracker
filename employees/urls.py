from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_employee, name='add_employee'),
    path('list/', views.employee_list, name='employee_list'),
    path('profile/<int:employee_id>/', views.employee_profile, name='employee_profile'),
    path('edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('reset-password/<int:employee_id>/', views.reset_password, name='reset_password'),
]
