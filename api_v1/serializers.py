from rest_framework import serializers

from axaxa.models import *

import datetime
import pytz


class LotSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cars
        fields = "__all__"
        read_only_fields = ('user', "slug")

    def validate(self, data):
        errors = {}
        if not AvailableCarList.objects.filter(brand=data['brand'],
                                               model=data['model'],
                                               generation=data['generation'],
                                               body=data['body']).exists():
            errors["car_name"] = "Car is not available for sale"
        if data['start_price'] < 0:
            errors["start_price"] = "Price must be greater than or equal to 0"
        current_time = datetime.datetime.now(pytz.utc)
        end_time = data.get('time_end')
        min_end_time = current_time + datetime.timedelta(days=2)
        if end_time <= min_end_time:
            errors["end_time"] = "Time of the auction can not be less then 3 days"
        if errors:
            raise serializers.ValidationError(errors)
        return data


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableCarList
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('post', 'user')


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = ('time', 'lot', 'user')

    def validate(self, data):
        lot_id = self.context['view'].kwargs['post_id']
        current_price = Cars.objects.get(id=lot_id).bid
        if data.get('price') <= current_price:
            raise serializers.ValidationError({'price': 'Bid is lower then expected'})
        return data
