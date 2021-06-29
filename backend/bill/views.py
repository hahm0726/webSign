from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BillSerializer
from .models import Bill



class BillViewSet(viewsets.ModelViewSet):
    """
    Defalut CRUD Bill viewset
    read - GET localhost:8000/bills/bill/<bill_id>/
    create - POST localhost:8000/bills/bill/ data:{}
    update - PATCH localhost:8000/bills/bill/<bill_id>/ data:{toChangeFieldName: value}
    delete - DELETE localhost:8000/bills/bill/<bill_id>/
    """

    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class BillListViewSet(viewsets.ModelViewSet):
    """
    Defalut CRUD Bill viewset
    read - GET localhost:8000/bills/bill-list/
    create - POST localhost:8000/bills/bill-list/ data:[{},{},...]
    update - PATCH localhost:8000/bills/bill-list/ data:[{toChangeFieldName: value},{},...]
    """

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    