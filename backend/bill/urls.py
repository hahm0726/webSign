from django.urls import path, include
from rest_framework import routers
from .views import BillViewSet, BillListViewSet, BillUpdateAPIView, BillDeleteAPIView

router = routers.SimpleRouter()
router.register(r"bill", BillViewSet)
# router.register(r"bill-list", BillListViewSet)

urlpatterns = [
    path("",include(router.urls)),
    path("bill-list/", BillUpdateAPIView.as_view()),
    path("bill-del/", BillDeleteAPIView.as_view())
]
