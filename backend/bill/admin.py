from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display=(
        "idx",
        "name",
        "birthDate",
        "location",
        "amount",
        "receiveDate",
        "state",
        "signature",
        "created",
        "updated"
        )

