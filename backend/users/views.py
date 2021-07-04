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
        try:
            if not username:
                return Response({"msg": "아이디를 입력해주세요"}, status=406)

            obj = models.User.objects.get(username=username)
            return Response({"msg": "사용중인 id 입니다."}, status=406)
        except models.User.DoesNotExist:
            return Response({"msg": "사용 가능한 id 입니다."}, status=200)