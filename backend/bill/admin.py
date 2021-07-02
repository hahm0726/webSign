from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "idx",
        "name",
        "birthDate",
        "location",
        "amount",
        "receivedDate",
        "signature",
        "created",
        "updated"
        )

