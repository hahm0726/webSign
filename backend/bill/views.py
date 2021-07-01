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
            bill = get_object_or_404(Bill, idx=data["idx"])

            if bill is None:
                Bill.objects.create(data)
            else:
                res = BillSerializer(bill, data, partial=True)
                if res.is_valid():
                    res.save()

        return Response({"msg": "성공"},status=200)


class BillDeleteAPIView(APIView):
    def post(self, request):
        print(request.data)
        for data in request.data:
            print("data:" + str(data))
            bill = get_object_or_404(Bill, idx=data)
        

            if bill:
                bill.delete()
        
        return Response({"msg": "성공"},status=200)
