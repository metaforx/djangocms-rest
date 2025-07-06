from rest_framework import serializers
from cms.plugin_pool import plugin_pool
from typing import Dict, Any

# CMS internal fields to exclude from all plugin schemas
EXCLUDE_CMS_PLUGIN_FIELDS = {
    "cmsplugin_ptr",
    "id",
    "parent",
    "creation_date",
    "changed_date",
    "position",
    "language",
    "placeholder",
}



def map_field_to_schema(field: serializers.Field, field_name: str = "") -> dict:
    """
    Map DRF field to simple JSON Schema definition for rendering.

    Args:
        field: DRF serializer field instance
        field_name: Name of the field (unused but kept for compatibility)

    Returns:
        dict: Basic JSON Schema definition for the field
    """
    # Basic type mapping
    if isinstance(field, serializers.IntegerField):
        schema = {"type": "integer"}
    elif isinstance(field, (serializers.FloatField, serializers.DecimalField)):
        schema = {"type": "number"}
    elif isinstance(field, serializers.BooleanField):
        schema = {"type": "boolean"}
    elif isinstance(field, serializers.ListField):
        schema = {"type": "array"}
    elif isinstance(field, (serializers.DictField, serializers.JSONField)):
        schema = {"type": "object"}
    elif isinstance(field, serializers.PrimaryKeyRelatedField):
        schema = {"type": "integer"}
    elif isinstance(field, serializers.DateField):
        schema = {"type": "string", "format": "date"}
    elif isinstance(field, serializers.DateTimeField):
        schema = {"type": "string", "format": "date-time"}
    elif isinstance(field, serializers.EmailField):
        schema = {"type": "string", "format": "email"}
    elif isinstance(field, serializers.URLField):
        schema = {"type": "string", "format": "uri"}
    elif isinstance(field, serializers.UUIDField):
        schema = {"type": "string", "format": "uuid"}
    elif isinstance(field, serializers.ChoiceField):
        schema = {"type": "string", "enum": list(field.choices.keys())}
    elif hasattr(field, "fields"):  # Nested serializer
        schema = {"type": "object"}
        # Extract nested properties
        properties = {}
        for nested_field_name, nested_field in field.fields.items():
            properties[nested_field_name] = map_field_to_schema(nested_field, nested_field_name)
        if properties:
            schema["properties"] = properties
    else:
        schema = {"type": "string"}

    # Description from help_text
    if getattr(field, "help_text", None):
        schema["description"] = str(field.help_text)

    return schema





def generate_plugin_definitions() -> Dict[str, Any]:
    """
    Generate simple plugin definitions for rendering.
    """
    definitions = {}

    for plugin in plugin_pool.get_all_plugins():
        # Use plugin's serializer_class or create a simple fallback
        serializer_cls = getattr(plugin, "serializer_class", None)

        if not serializer_cls:
            class DynamicModelSerializer(serializers.ModelSerializer):
                class Meta:
                    model = plugin.model
                    fields = "__all__"
            serializer_cls = DynamicModelSerializer

        try:
            serializer_instance = serializer_cls()
            properties = {}

            for field_name, field in serializer_instance.fields.items():
                # Skip internal CMS fields
                if field_name in EXCLUDE_CMS_PLUGIN_FIELDS:
                    continue

                properties[field_name] = map_field_to_schema(field, field_name)

            definitions[plugin.__name__] = {
                "name": getattr(plugin, "name", plugin.__name__),
                "type": "object",
                "properties": properties,
            }

        except Exception:
            # Skip plugins that fail to process
            continue

    return definitions
