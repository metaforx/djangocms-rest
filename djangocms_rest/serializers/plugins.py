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
        dict: Basic JSON Schema definition for the field for TypeScript compatibility
    """

    # Field type mapping for TypeScript compatibility
    field_mapping = {
        "CharField": {"type": "string"},
        "TextField": {"type": "string"},
        "URLField": {"type": "string"},
        "EmailField": {"type": "string"},
        "IntegerField": {"type": "integer"},
        "FloatField": {"type": "number"},
        "DecimalField": {"type": "number"},
        "BooleanField": {"type": "boolean"},
        "DateField": {"type": "string"},
        "DateTimeField": {"type": "string"},
        "TimeField": {"type": "string"},
        "FileField": {"type": "string"},
        "ImageField": {"type": "string"},
        "JSONField": {"type": "object"},
        "ForeignKey": {"type": "integer"},
        "PrimaryKeyRelatedField": {"type": "integer"},
        "ListField": {"type": "array"},
        "DictField": {"type": "object"},
        "UUIDField": {"type": "string"},
    }

    # Handle special cases first
    if isinstance(field, serializers.ChoiceField):
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
        # Use mapping or default to string
        schema = field_mapping.get(field.__class__.__name__, {"type": "string"})

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
