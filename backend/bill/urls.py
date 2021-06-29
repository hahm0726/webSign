from django.urls import path, include
from rest_framework import routers
from .views import BillViewSet, BillListViewSet

router = routers.SimpleRouter()
router.register(r"bill", BillViewSet)
router.register(r"bill-list", BillListViewSet)

urlpatterns = [
    path("",include(router.urls)),
]
