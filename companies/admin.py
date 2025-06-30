from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'admin', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'admin__username')
    readonly_fields = ('created_at', 'updated_at')
