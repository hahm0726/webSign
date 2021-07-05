from django.urls import include, path
from rest_framework import routers, urlpatterns
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = routers.SimpleRouter()
router.register(r"user", views.UserViewSet)

urlpatterns = [
    path("login/", views.login),  # 로그인 경로
    path("refresh/", TokenRefreshView.as_view()),  # 액세스 토큰 재 발급경로
    path("api/", include(router.urls))
]