import rest_framework.permissions
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.permissions import IsAdminOrReadOnly
from api_v1.serializers import *
from axaxa.models import *


class APIListDefaultPagination(PageNumberPagination):
    page_size = 3


class LotList(generics.ListCreateAPIView):
    """ Return's lot's list """
    queryset = Cars.objects.all()
    serializer_class = LotSerializer
    pagination_class = APIListDefaultPagination
    permission_class = (IsAuthenticatedOrReadOnly,)


class CarsList(generics.ListCreateAPIView):
    """ Return's car's list that supported on web-site """
    queryset = AvailableCarList.objects.all()
    serializer_class = CarSerializer
    pagination_class = APIListDefaultPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FindCarList(APIView):
    """ Return's lot or lot's using parameters:
        brand / brand and model / brand and model and max price """
    def get(self, request, brand, model=None, max_price=None):
        if model is None:
            model.replace("_", " ")
            query = Cars.objects.filter(brand__iexact=brand)
        else:
            if max_price:
                query = Cars.objects.filter(brand__iexact=brand.replace("_", " "),
                                            model__iexact=model.replace("_", " "),
                                            bid__lte=max_price)
            else:
                query = Cars.objects.filter(brand__iexact=brand.replace("_", " "),
                                            model__iexact=model.replace("_", " "))
        if query:
            serializer = LotSerializer(query, many=True)
            return Response(serializer.data)
        return Response(status=400, data={'No matches'})
