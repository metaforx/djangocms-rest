
import json
from typing import Any, Callable, Dict, Optional, TypeVar

from django.db import models
from django.utils.html import escape, mark_safe

from cms.plugin_rendering import ContentRenderer
from rest_framework import serializers


base_exclude = {
    "id",
    "placeholder",
    "language",
    "position",
    "creation_date",
    "changed_date",
    "parent",
}


ModelType = TypeVar("ModelType", bound=models.Model)


def get_auto_model_serializer(model_class: type[ModelType]) -> type:
    """
    Build (once) a generic ModelSerializer subclass that excludes
    common CMS bookkeeping fields.
    """


    opts = model_class._meta
    real_fields = {f.name for f in opts.get_fields()}
    exclude = tuple(base_exclude & real_fields)

    meta_class = type(
        "Meta",
        (),
        {
            "model": model_class,
            "exclude": exclude,
        },
    )
    return type(
        f"{model_class.__name__}AutoSerializer",
        (serializers.ModelSerializer,),
        {
            "Meta": meta_class,
        },
    )


def render_cms_plugin(instance: Optional[Any], context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not instance or not hasattr(instance, "get_plugin_instance"):
        return None

    try:
        plugin_instance, plugin = instance.get_plugin_instance()
    except (AttributeError, TypeError):
        return None

    if not plugin_instance:
        return None

    model_cls = plugin_instance.__class__
    serializer_cls = getattr(plugin, "serializer_class", None)
    serializer_cls = serializer_cls or get_auto_model_serializer(model_cls)

    return serializer_cls(plugin_instance, context=context).data


class RESTRenderer(ContentRenderer):
    """
    A custom renderer that uses the render_cms_plugin function to render
    CMS plugins in a RESTful way.
    """

    def render_plugin(self, instance, context, placeholder=None, editable=False):
        """
        Render a CMS plugin instance using the render_cms_plugin function.
        """
        content = self.pretty_print_data(instance, context)
        if editable:
            content = self.plugin_edit_template.format(
                pk=instance.pk,
                placeholder=instance.placeholder_id,
                content=content,
                position=instance.position
            )
            placeholder_cache = self._rendered_plugins_by_placeholder.setdefault(
                placeholder.pk, {}
            )
            placeholder_cache.setdefault("plugins", []).append(instance)
        return mark_safe(content)

    def pretty_print_data(self, instance, context):
        """
        Convert the plugin instance data to a pretty-printed JSON string.
        """
        data = render_cms_plugin(instance, context) or {}

        # Use json.dumps to convert the data to a JSON string
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        return escape(json_data)