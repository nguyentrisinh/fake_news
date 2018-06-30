from rest_framework import serializers


class AccuracySerializer(serializers.Serializer):
    result = serializers.CharField()
    elapsed_time = serializers.CharField()
