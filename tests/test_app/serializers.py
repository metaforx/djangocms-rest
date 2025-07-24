from rest_framework import serializers


class CustomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    integer = serializers.IntegerField(default=42)
    float = serializers.FloatField(default=3.14)
    title = serializers.ChoiceField(
        choices=["title", "subtitle", "header"],
        default="title",
    )
    json = serializers.JSONField()

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "integer": 42,
            "float": 3.14,
            "title": "title",
            "json": [
                {"key": "value"},
                {"another_key": "another_value"},
                [1, 2, 3, 4, 5],
                True,
                False,
                None,
            ],
        }
