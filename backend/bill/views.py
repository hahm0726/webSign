from functools import partial
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BillSerializer,BillListSerializer
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
    serializer_class = BillListSerializer
    

class BillUpdateAPIView(APIView):
    def post(self, request):

        for data in request.data:
            
            if data["id"] is None:
                del data["id"]
                res = BillSerializer(data=data)
                if res.is_valid():
                    res.save()
            else:
                bill = get_object_or_404(Bill, id=data["id"])
                res = BillSerializer(bill, data, partial=True)
                if res.is_valid():
                    res.save()

        return Response({"msg": "성공"},status=200)


class BillDeleteAPIView(APIView):
    def post(self, request):
        for id in request.data:
            bill = get_object_or_404(Bill, id=id)
        

            if bill:
                bill.delete()
        
        return Response({"msg": "성공"},status=200)
