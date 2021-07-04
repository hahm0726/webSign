from django.urls import include, path
from rest_framework import routers, urlpatterns
from . import views

router = routers.SimpleRouter()
router.register(r"user", views.UserViewSet)

urlpatterns = [
    path("api/", include(router.urls))
]