from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # csrf 회피용 (테스트)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken  # 토큰 발행 위한 라이브러리
from . import models, serializers

# 토큰 발급 함수
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)  # 데이터 JSON으로 파싱
        input_id = data["username"]
        input_pw = data["password"]

        if not input_id or not input_pw:
            return JsonResponse({"msg": "값을 모두 입력해주세요"}, status=400)

        # 장고 유저인증 사용하여 인증(성공시 id 반환, 실패시 None 반환)
        login_res = authenticate(username=input_id, password=input_pw)
        
        if login_res:
            # JWT 토큰 생성
            tokens = get_tokens_for_user(login_res)
            print(login_res.id)
            update_last_login(None, login_res)  # 마지막 로그인 시간 업데이트
            # 프론트 서버로 보낼 데이터 정의
            req_data = {
                "msg": "로그인 성공",
                "user_id": login_res.id,
                "userType": login_res.userType,
            }
            req_data["tokens"] = tokens  # 반환 데이터 딕셔너리 병합
            return JsonResponse(req_data, status=200)
        else:
            return JsonResponse({"msg": "비밀번호가 틀렸습니다."}, status=401)

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