from rest_framework import serializers


class CustomSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "integer": 42,
            "float": 3.14,
            "json": [
                {"key": "value"},
                {"another_key": "another_value"},
                [1, 2, 3, 4, 5],
                True,
                False,
                None,
            ],
        }
