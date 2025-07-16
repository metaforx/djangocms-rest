from typing import Any, Optional

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Field, Model
from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse

from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool

from djangocms_rest.utils import get_absolute_frontend_url
from rest_framework import serializers


def serialize_fk(
    request: HttpRequest,
    related_model: type[CMSPlugin],
    pk: Any,
    obj: Optional[Model] = None,
) -> dict[str, Any]:
    """
    Serializes a foreign key reference to a related model as a URL or identifier.

    Attempts to serialize the foreign key in the following order:
    1. If the related model has a `get_api_endpoint` method, it uses this to obtain the API endpoint for the object.
    2. If not, it tries to reverse a DRF-style detail URL using the model's name and primary key.
    3. If reversing fails, it falls back to returning a string in the format "<app_label>.<model_name>:<pk>".

    Args:
        related_model (type[CMSPlugin]): The related model class.
        pk (Any): The primary key of the related object.
        obj (Optional[Model], optional): The related model instance, if already available. Defaults to None.

    Returns:
        dict[str, Any]: A dictionary representing the serialized foreign key, typically as a URL or identifier.
    """
    # First choice: Check for get_api_endpoint method
    if hasattr(related_model, "get_api_endpoint"):
        if obj is None:
            obj = related_model.objects.filter(pk=pk).first()
        return get_absolute_frontend_url(request, obj.get_api_endpoint())

    # Second choice: Use DRF naming conventions to build the default API URL for the related model
    model_name = related_model._meta.model_name
    try:
        return get_absolute_frontend_url(
            request, reverse(f"{model_name}_details", args=(pk,))
        )
    except NoReverseMatch:
        pass

    # Fallback:
    app_name = related_model._meta.app_label
    return f"{app_name}.{model_name}:{pk}"


def serialize_soft_refs(request: HttpRequest, data: Any) -> Any:
    """
    Serialize soft references in a dictionary or list.

    This function recursively traverses the input data structure and serializes
    any soft references (dictionaries with 'model' and 'pk' keys) into a more
    usable format.

    Args:
        data (Any): The input data structure, which can be a dict, list, or other types.

    Returns:
        Any: The serialized data structure with soft references replaced.
    """
    if isinstance(data, list):
        return [serialize_soft_refs(request, item) for item in data]
    for key, value in data.items():
        if isinstance(value, dict) and set(value.keys()) == {"model", "pk"}:
            app_name, model_name = value["model"].split(".", 1)
            model_class = apps.get_model(app_name, model_name)
            pk = value["pk"]
            data[key] = serialize_fk(request, model_class, pk)
        elif key == "attrs" and isinstance(value, dict) and value.get("data-cms-href"):
            model, pk = value["data-cms-href"].split(":", 1)
            app_name, model_name = model.split(".", 1)
            model_class = apps.get_model(app_name, model_name)
            value["data-cms-href"] = serialize_fk(request, model_class, pk)
        elif isinstance(value, dict) and "internal_link" in value:
            model, pk = value["internal_link"].split(":", 1)
            app_name, model_name = model.split(".", 1)
            model_class = apps.get_model(app_name, model_name)
            data[key] = serialize_fk(request, model_class, pk)
        elif isinstance(value, dict) and "file_link" in value:
            model_class = apps.get_model("filer", "file")
            data[key] = serialize_fk(request, model_class, value["file_link"])
        elif isinstance(value, (dict, list)):
            data[key] = serialize_soft_refs(request, value)
    return data


base_exclude = {
    "id",
    "placeholder",
    "language",
    "position",
    "creation_date",
    "changed_date",
    "parent",
}
#: Excluded fields for plugin serialization

JSON_FIELDS = tuple(
    field
    for field, value in serializers.ModelSerializer.serializer_field_mapping.items()
    if value is serializers.JSONField
)


class GenericPluginSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request", None)

    def to_representation(self, instance: CMSPlugin):
        request = getattr(self, "request", None)

        ret = super().to_representation(instance)
        for field in self.Meta.model._meta.get_fields():
            if field.is_relation and not field.many_to_many and not field.one_to_many:
                if field.name in ret and getattr(instance, field.name, None):
                    ret[field.name] = serialize_fk(
                        request,
                        field.related_model,
                        getattr(instance, field.name + "_id"),
                        obj=getattr(instance, field.name)
                        if field.is_cached(instance)
                        else None,
                    )
            elif isinstance(field, JSON_FIELDS) and ret.get(field.name):
                # If the field is a subclass of JSONField, serialize its value directly
                ret[field.name] = serialize_soft_refs(request, ret[field.name])
        return ret


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
