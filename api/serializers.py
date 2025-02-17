from .models import StockCompany, StockRating
from rest_framework import serializers
from django.contrib.auth.models import User
# Serializer for StockCompany Model


class StockCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCompany
        fields = ('id', 'name', 'description',
                  'industry', 'market_cap', 'created_at', 'average_rating')

# Serializer for StockRating Model


class StockRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRating
        fields = ('id', 'company', 'user', 'rating', 'comment', 'created_at')

# Nested Serializer: Shows stock ratings inside StockCompany response


class StockCompanyDetailSerializer(serializers.ModelSerializer):
    ratings = StockRatingSerializer(
        many=True, read_only=True, source='stockrating_set')

    class Meta:
        model = StockCompany
        fields = ('id', 'name', 'description', 'industry',
                  'market_cap', 'created_at', 'ratings')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
