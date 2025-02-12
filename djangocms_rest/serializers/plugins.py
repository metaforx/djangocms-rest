from rest_framework import serializers
from cms.plugin_pool import plugin_pool
from django.core.exceptions import FieldDoesNotExist

class PluginDefinitionSerializer(serializers.Serializer):
    """Serializer for plugin type definitions"""
    plugin_type = serializers.CharField(help_text="Unique identifier for the plugin type")
    title = serializers.CharField(help_text="Human readable name of the plugin")
    type = serializers.CharField(help_text="Schema type")
    properties = serializers.DictField(help_text="Property definitions")

def get_field_type(field):
    """Convert Django field types to JSON Schema types"""
    field_mapping = {
        'CharField': 'string',
        'TextField': 'string',
        'URLField': 'string',
        'EmailField': 'string',
        'IntegerField': 'integer',
        'FloatField': 'number',
        'DecimalField': 'number',
        'BooleanField': 'boolean',
        'DateField': 'string',
        'DateTimeField': 'string',
        'TimeField': 'string',
        'FileField': 'string',
        'ImageField': 'string',
        'JSONField': 'object',
        'ForeignKey': 'integer',
    }
    return field_mapping.get(field.__class__.__name__, 'string')

def get_field_format(field):
    """Get the format for specific field types"""
    format_mapping = {
        'URLField': 'uri',
        'EmailField': 'email',
        'DateField': 'date',
        'DateTimeField': 'date-time',
        'TimeField': 'time',
        'FileField': 'uri',
        'ImageField': 'uri',
    }
    return format_mapping.get(field.__class__.__name__)

def generate_plugin_definitions():
    """Generate plugin definitions from registered plugins"""
    definitions = {}

    # Fields to exclude from the schema
    excluded_fields = {
        'cmsplugin_ptr',
        'id',
        'parent',
        'creation_date',
        'changed_date',
        'position',
        'language',
        'plugin_type',  # We'll add this manually
        'placeholder',
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
                    "description": str(getattr(model_field, 'help_text', '') or '')
                }

                # Add format if applicable
                field_format = get_field_format(model_field)
                if field_format:
                    field_def["format"] = field_format

                properties[field.name] = field_def

                # Add to required fields if not nullable
                if not getattr(model_field, 'blank', True):
                    required.append(field.name)

            except FieldDoesNotExist:
                continue

        # Add plugin_type to properties and required
        properties["plugin_type"] = {
            "type": "string",
            "const": plugin.__name__,
            "description": "Plugin identifier"
        }
        required.append("plugin_type")

        definitions[plugin.__name__] = {
            "title": getattr(plugin_class, 'name', plugin.__name__),
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False
        }

    return definitions

# Generate plugin definitions
PLUGIN_DEFINITIONS = generate_plugin_definitions()
