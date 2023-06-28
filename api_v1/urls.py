from django.urls import path

from api_v1.views import *

urlpatterns = [
    path('api/v1/lot', LotList.as_view()),
    path('api/v1/car', CarsList.as_view()),
    path('api/v1/<str:brand>', FindCarList.as_view()),
    path('api/v1/<str:brand>/<str:model>', FindCarList.as_view()),
    path('api/v1/<str:brand>/<str:model>/<int:max_price>', FindCarList.as_view()),
]