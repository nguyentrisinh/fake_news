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


class ListNewsDetailSerializer(serializers.Serializer):
    details = serializers.ListField(child=serializers.CharField())


class PredictedResultSerializer(serializers.Serializer):
    predicted_result = serializers.ListField(child=serializers.CharField())
    elapsed_time = serializers.CharField()


class FakeNewsPredictedResultSerializer(serializers.Serializer):
    predicted_result = serializers.ListField(child=serializers.IntegerField())
    elapsed_time = serializers.CharField()