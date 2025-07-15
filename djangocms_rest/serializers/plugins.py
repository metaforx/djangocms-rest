from typing import Any, Optional

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Field

from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool

from rest_framework import serializers


class GenericPluginSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: CMSPlugin):
        ret = super().to_representation(instance)
        for field in self.Meta.model._meta.get_fields():
            if field.is_relation and not field.many_to_many and not field.one_to_many:
                field_name = field.name
                if field_name in ret and getattr(instance, field_name, None):
                    ret[field_name] = self.serialize_fk(field)
        return ret

    def serialize_fk(self, related_obj):
        pass


class PluginDefinitionSerializer(serializers.Serializer):
    """
    Serializer for plugin type definitions.
    """

    plugin_type = serializers.CharField(
        help_text="Unique identifier for the plugin type"
    )
    title = serializers.CharField(help_text="Human readable name of the plugin")
    type = serializers.CharField(help_text="Schema type")
    properties = serializers.DictField(help_text="Property definitions")


def get_field_type(field: Field) -> str:
    """
    Convert Django field types to JSON Schema types.

    Args:
        field (Field): Django model field instance

    Returns:
        str: JSON Schema type corresponding to the Django field type
    """
    field_mapping = {
        "CharField": "string",
        "TextField": "string",
        "URLField": "string",
        "EmailField": "string",
        "IntegerField": "integer",
        "FloatField": "number",
        "DecimalField": "number",
        "BooleanField": "boolean",
        "DateField": "string",
        "DateTimeField": "string",
        "TimeField": "string",
        "FileField": "string",
        "ImageField": "string",
        "JSONField": "object",
        "ForeignKey": "integer",
    }
    return field_mapping.get(field.__class__.__name__, "string")


def get_field_format(field: Field) -> Optional[str]:
    """
    Get the format for specific field types.

    Args:
        field (Field): Django model field instance

    Returns:
        Optional[str]: JSON Schema format string if applicable, None otherwise
    """
    format_mapping = {
        "URLField": "uri",
        "EmailField": "email",
        "DateField": "date",
        "DateTimeField": "date-time",
        "TimeField": "time",
        "FileField": "uri",
        "ImageField": "uri",
    }
    return format_mapping.get(field.__class__.__name__)


def generate_plugin_definitions() -> dict[str, Any]:
    """
    Generate plugin definitions from registered plugins.

    Returns:
        Dict[str, Any]: A dictionary mapping plugin types to their definitions.
        Each definition contains:
            - title: Human readable name
            - type: Schema type (always "object")
            - properties: Field definitions following JSON Schema format
            - required: List of required field names
    """
    definitions = {}

    excluded_fields = {
        "cmsplugin_ptr",
        "id",
        "parent",
        "creation_date",
        "changed_date",
        "position",
        "language",
        "plugin_type",
        "placeholder",
    }

    for plugin in plugin_pool.get_all_plugins():
        model = plugin.model
        plugin_class = plugin_pool.get_plugin(plugin.__name__)

        properties = {}
        required = []

        # Get fields from the model
        for field in model._meta.get_fields():
            # Skip excluded and relation fields
            if field.name in excluded_fields or field.is_relation:
                continue

            try:
                model_field = model._meta.get_field(field.name)
                field_def = {
                    "type": get_field_type(model_field),
                    "description": str(getattr(model_field, "help_text", "") or ""),
                }

                # Add format if applicable
                field_format = get_field_format(model_field)
                if field_format:
                    field_def["format"] = field_format

                properties[field.name] = field_def

                # Add to required fields if not nullable
                if not getattr(model_field, "blank", True):
                    required.append(field.name)

            except FieldDoesNotExist:
                continue

        # Add plugin_type to properties and required
        properties["plugin_type"] = {
            "type": "string",
            "const": plugin.__name__,
            "description": "Plugin identifier",
        }
        required.append("plugin_type")

        definitions[plugin.__name__] = {
            "title": getattr(plugin_class, "name", plugin.__name__),
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        }

    return definitions


# Generate plugin definitions
PLUGIN_DEFINITIONS = generate_plugin_definitions()
