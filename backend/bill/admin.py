from django.contrib import admin
from .models import Bill


@admin.register(Bill)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "정보",
            {
                "fields": ["idx", "name", "birthDate", "location", "amount", "receiveDate", "state"]
            }
        )
    ]
