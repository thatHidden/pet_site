import rest_framework.permissions
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *

from api_v1.permissions import IsAdminOrReadOnly
from api_v1.serializers import *
from axaxa.models import *


class APIListDefaultPagination(PageNumberPagination):
    page_size = 3


class LotList(generics.ListCreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = LotSerializer
    pagination_class = APIListDefaultPagination
    permission_class = (IsAuthenticatedOrReadOnly, )


class CarsList(generics.ListCreateAPIView):
    queryset = AvailableCarList.objects.all()
    serializer_class = CarSerializer
    pagination_class = APIListDefaultPagination
    permission_classes = (IsAuthenticatedOrReadOnly, )
