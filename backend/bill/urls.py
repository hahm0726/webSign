from django.urls import path, include
from rest_framework import routers
from .views import BillViewSet

router = routers.SimpleRouter()
router.register(r"", BillViewSet)

urlpatterns = [
    path("",include(router.urls)),
]
