from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BillSerializer
from .models import Bill



class BillViewSet(viewsets.ModelViewSet):
    """
    Defalut CRUD Bill viewset
    read - GET localhost:8000/bill/<bill_id>/
    create - POST localhost:8000/bill/
    update - PATCH localhost:8000/bill/<bill_id>/ data:{toChangeFieldName: value}
    delete - DELETE localhost:8000/bill/<bill_id>/
    """

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    