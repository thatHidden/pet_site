from django.urls import path

from api_v1.views import *

urlpatterns = [
    path('api/v1/lot', LotList.as_view()),
    path('api/v1/car', CarsList.as_view()),
]