from rest_framework import serializers


class CustomSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "integer": 42,
            "float": 3.14,
        }
