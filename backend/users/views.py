from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from . import models, serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    # url: users/api/user/chk_username/
    @action(detail=False, methods=['get'])
    def chk_username(self, request):
        username = request.GET.get('username')
        print(username)
        try:
            obj = models.User.objects.get(username=username)
            return Response({"state": "1"}, status=200)
        except models.User.DoesNotExist:
            return Response({"state": "0"}, status=200)