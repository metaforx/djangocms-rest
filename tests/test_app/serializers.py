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
    # Exercises base_exclude skip in schema generation; see test_plugin_list.
    position = serializers.IntegerField(default=0)

    class KeyValuePairSerializer(serializers.Serializer):
        prop1 = serializers.CharField()
        prop2 = serializers.CharField()
        prop3 = serializers.CharField()

    kvp = KeyValuePairSerializer()

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
            "kvp": {
                "prop1": "value1",
                "prop2": "value2",
                "prop3": "value3",
            },
        }
