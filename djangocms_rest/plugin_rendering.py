
from typing import Any, Dict, Iterable, Optional, TypeVar

from django.db import models
from django.utils.html import escape, mark_safe

from cms.plugin_rendering import ContentRenderer
from rest_framework import serializers

from djangocms_rest.serializers.placeholders import PlaceholderSerializer


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


def highlight_data(json_data: Any) -> str:
    """
    Highlight JSON data using Pygments.
    """
    if isinstance(json_data, str):
        classes = "str"
        if len(json_data) > 100:
            classes += " ellipsis"
        return f'<span class="{classes}">"{escape(json_data)}"</span>'
    if isinstance(json_data, (int, float)):
        return f'<span class="num">{json_data}</span>'
    if isinstance(json_data, bool):
        return f'<span class="bool">{str(json_data).lower()}</span>'
    if json_data is None:
        return '<span class="null">null</span>'
    if isinstance(json_data, dict):
        return highlight_json(json_data)
    if isinstance(json_data, list):
        return highlight_list(json_data)

    return f'<span class="obj">{json_data}</span>'

def highlight_json(json_data: Dict[str, Any], children: Iterable|None = None, field: str = "children") -> str:
    has_children = children is not None
    if field in json_data:
        del json_data[field]

    if not json_data and not has_children:
        return "{}"
    items = [
        f'<div class="js-kvp"><span class="key">"{escape(key)}"</span>: {highlight_data(value)},</div>'
        for key, value in json_data.items()
    ]
    if has_children:
        rendered_children = f'<div class="js-kvp"><span class="children">"{field}"</span>: [<div class="indent">{"".join(children)}</div></div>]'
        items.append(rendered_children)
    return f'{{<div class="indent">{"".join(items)}</div>}}'

def highlight_list(json_data: list) -> str:
    items = [highlight_data(item) for item in json_data]
    return f'[<div class="indent">{",<br>".join(items)}</div>]'


class RESTRenderer(ContentRenderer):
    """
    A custom renderer that uses the render_cms_plugin function to render
    CMS plugins in a RESTful way.
    """

    def render_plugin(self, instance, context, placeholder=None, editable: bool = False):
        """
        Render a CMS plugin instance using the render_cms_plugin function.
        """
        data = render_cms_plugin(instance, context) or {}
        children = [
            self.render_plugin(child, context, placeholder=placeholder, editable=editable)
            for child in getattr(instance, 'child_plugin_instances', [])
        ] or None
        content = highlight_json(data, children=children)

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

    def render_plugins(self, placeholder, language, context, editable=False, template=None):
        yield "<div class='rest-placeholder' data-placeholder='{placeholder}' data-language='{language}'>".format(
            placeholder=placeholder.slot,
            language=language,
        )
        placeholder_data = PlaceholderSerializer(instance=placeholder, language=language, request=context["request"], render_plugins=False).data

        yield highlight_json(
            placeholder_data,
            children=super().render_plugins(
                placeholder, language, context, editable=editable, template=template
            ),
            field="content",
        )
        yield "</div>"
