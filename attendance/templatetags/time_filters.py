from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def seconds_to_hours(seconds):
    """Convert seconds to hours with 1 decimal place"""
    if not seconds:
        return "0.0"
    
    try:
        # Handle both integer seconds and timedelta objects
        if isinstance(seconds, timedelta):
            total_seconds = seconds.total_seconds()
        else:
            total_seconds = float(seconds)
            
        hours = total_seconds / 3600
        return f"{hours:.1f}"
    except (ValueError, TypeError, AttributeError):
        return "0.0"

@register.filter
def percentage(value, total):
    """Calculate percentage with 1 decimal place"""
    if not value or not total or total == 0:
        return "0.0"
    
    try:
        value = float(value)
        total = float(total)
        percent = (value / total) * 100
        return f"{percent:.1f}"
    except (ValueError, TypeError):
        return "0.0"

@register.filter
def attendance_percentage(present_days, total_days=30):
    """Calculate attendance percentage"""
    return percentage(present_days, total_days)
