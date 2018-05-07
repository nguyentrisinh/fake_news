from rest_framework import serializers

from ..models import NewsDetail


class BaseNewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsDetail
        # fields = '__all__'
        exclude = ('created_at', 'updated_at')


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsDetail
        fields = ('details',)
