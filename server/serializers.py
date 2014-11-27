from rest_framework import serializers
from server.models import User, Listing

__author__ = 'simone'


class UserSerializer(serializers.ModelSerializer):
    city_name = serializers.Field(source='city.name')

    class Meta:
        model = User
        fields = (
            'username', 'password', 'email', 'address', "city", 'city_name', 'is_admin', 'is_active', 'available_hours',
            'worked_hours',
            'requested_hours', 'used_hours')
        write_only_fields = ('password',)


class ListingSerializer(serializers.ModelSerializer):
    category_name = serializers.Field(source='category.name')

    class Meta:
        model = Listing
        fields = ('id','creation_date', 'description', 'category', 'category_name', 'owner', 'applicant', 'requested')

