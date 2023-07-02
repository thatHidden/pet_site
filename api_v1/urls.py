from django.urls import path

from api_v1.views import *

urlpatterns = [
    path('lot/', LotList.as_view()),
    path('car/', CarsList.as_view()),
    path('<str:brand>/', FindCarList.as_view()),
    path('<str:brand>/<str:model>/', FindCarList.as_view()),
    path('<str:brand>/<str:model>/<int:max_price>/', FindCarList.as_view()),
]