import sys

import rest_framework.permissions
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.mixins import MultipleFieldLookupMixin
from api_v1.permissions import *
from api_v1.serializers import *
from axaxa.models import *


class APIListDefaultPagination(PageNumberPagination):
    page_size = 5


class CreateGetComment(generics.CreateAPIView, generics.ListAPIView):
    """
    Create or Get comments for a specific post.

    GET: send GET request.

    CREATE: send POST request. Only for authenticated users. Must include JSON
    {
        "content": "<text of comment>"
    }

    HTTP methods supported: POST and GET.
    """
    queryset = Comment.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = APIListDefaultPagination

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        queryset = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(user=self.request.user, post=Cars.objects.get(id=post_id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetUpdateDeleteComment(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Get or Update or Delete specific comment.

    GET: send GET request;

    Delete: send DELETE request. Only for staff and comment owner.

    Update: send UPDATE request. Only for comment owner. Must include JSON
    {
        "content": "<text of comment>"
    }

    HTTP methods supported: GET, UPDATE, DELETE.
    """
    queryset = Comment.objects.all()
    http_method_names = ['get', 'put', 'delete']
    serializer_class = CommentSerializer
    lookup_fields = ['post_id', 'id']
    pagination_class = APIListDefaultPagination

    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = [IsOwnerOrReadOnly, ]
        else:
            self.permission_classes = [IsOwnerOrAdminOrReadOnly, ]
        return super(GetUpdateDeleteComment, self).get_permissions()


class GetUpdateDeleteLot(generics.RetrieveUpdateDestroyAPIView):
    """
    Get or Update or Delete specific lot.

    GET: send GET request;

    Delete: send DELETE request. Only for staff and comment owner.

    Update: send UPDATE request. Only for comment owner. Must include JSON
    {
        "brand": "<brand name>"
        "model": "<model name>"
        "generation": <generation of model>
        "body": "<body-type>"
        "description": "<lot description>"
        "time_end": <YYYY-MM-DD HH:mm:ss>
        "start_price": <start price, int>
       *"photo": <car photo>
    }
    * not required

    HTTP methods supported: GET, UPDATE, DELETE.
    """
    queryset = Cars.objects.all()
    http_method_names = ['get', 'put', 'delete']
    serializer_class = LotSerializer
    lookup_field = "id"
    pagination_class = APIListDefaultPagination

    def get_permissions(self):
        print(sys.version)
        if self.request.method == 'PUT':
            self.permission_classes = [IsOwnerOrReadOnly, ]
        else:
            self.permission_classes = [IsOwnerOrAdminOrReadOnly, ]
        return super(GetUpdateDeleteLot, self).get_permissions()


class CreateGetLot(generics.CreateAPIView, generics.ListAPIView):
    """
    Create or Get specific lot.

    Get: send GET request;

    Create: send POST request. Only for authenticated users. Must include JSON
    {
        "brand": "<brand name>"
        "model": "<model name>"
        "generation": <generation of model>
        "body": "<body-type>"
        "description": "<lot description>"
        "time_end": <YYYY-MM-DD HH:mm:ss>
        "start_price": <start price, int>
       *"photo": <car photo>
    }
    * not required

    HTTP methods supported: GET and POST.
    """
    queryset = Cars.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = LotSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = APIListDefaultPagination

    def perform_create(self, serializer):
        brand = self.request.POST.get('brand')
        model = self.request.POST.get('model')
        generation = self.request.POST.get('generation')
        start_price = self.request.POST.get('start_price')
        while True:
            characters = string.ascii_uppercase + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(4))
            slug = random_string + "-" + slugify(brand + "-" +
                                                 model + "-" +
                                                 (generation if generation != "1" else ""))
            if not Cars.objects.filter(slug=slug).exists():
                break
        serializer.save(user=self.request.user,
                        bid=start_price,
                        slug=slug
                        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateGetBid(generics.CreateAPIView, generics.ListAPIView):
    """
    Create or Get specific bid.

    Get: send GET request

    Create: send POST request. Only for authenticated users. Must include JSON
    {
        "price": <bid price, int>
    }

    HTTP methods supported: GET and POST.
    """
    queryset = Bid.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = BidSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = APIListDefaultPagination

    def perform_create(self, serializer):
        lot = Cars.objects.get(id=5)
        lot.bid_holder = self.request.user
        lot.bid = self.request.POST.get('price')
        lot.save()
        serializer.save(user=self.request.user,
                        lot_id=self.kwargs['post_id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        queryset = Bid.objects.filter(lot_id=post_id)
        serializer = BidSerializer(queryset, many=True)
        return Response(serializer.data)


class CarsList(generics.ListCreateAPIView):
    """
    Get list of lots

    Get: send GET request
    """
    http_method_names = ['get']
    queryset = AvailableCarList.objects.all()
    serializer_class = CarSerializer
    pagination_class = APIListDefaultPagination
    permission_classes = (AllowAny,)


class FindCarList(APIView):
    """
    Get list of lots wit specified params

    Get: send GET request

    Note: Return's lot or lot's using parameters:
    brand / brand and model / brand and model and max price
    """
    http_method_names = ['get']

    def get(self, request, brand, model=None, max_price=None):
        if model is None:
            brand.replace("_", " ")
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
