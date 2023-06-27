from rest_framework import serializers

from axaxa.models import *


class LotSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cars
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = AvailableCarList
        fields = "__all__"
