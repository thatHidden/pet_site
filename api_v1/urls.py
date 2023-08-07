from django.template.defaulttags import url
from django.urls import path, include, re_path

from api_v1.views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('lots/', CreateGetLot.as_view()),
    path('cars/', CarsList.as_view()),

    path('lots/<int:id>/', GetUpdateDeleteLot.as_view()),

    path('lots/<int:pk>/comments/', CreateGetComment.as_view()),
    path('lots/<int:post_id>/comments/<int:id>/', GetUpdateDeleteComment.as_view()),

    path('lots/<int:post_id>/bids/', CreateGetBid.as_view()),
    # path('lots/<int:post_id>/bids/<int:id>/', GetUpdateDeleteBid.as_view()),

    path('lots/<str:brand>/', FindCarList.as_view()),
    path('lots/<str:brand>/<str:model>/', FindCarList.as_view()),
    path('lots/<str:brand>/<str:model>/<int:max_price>/', FindCarList.as_view()),
]