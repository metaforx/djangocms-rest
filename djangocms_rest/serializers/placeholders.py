from django.template import Context
from rest_framework import serializers

from djangocms_rest.serializers.utils.render import render_html


class PlaceholderSerializer(serializers.Serializer):
    slot = serializers.CharField()
    label = serializers.CharField()
    language = serializers.CharField()
    content = serializers.ListSerializer(
        child=serializers.JSONField(), allow_empty=True, required=False
    )
    html = serializers.CharField(default="", required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        placeholder = kwargs.pop("instance", None)
        language = kwargs.pop("language", None)
        render_plugins = kwargs.pop("render_plugins", True)
        super().__init__(*args, **kwargs)

        if placeholder and request and language:
            if render_plugins:
                from djangocms_rest.plugin_rendering import RESTRenderer

                renderer = RESTRenderer(request)
                placeholder.content = renderer.serialize_placeholder(
                    placeholder,
                    context=Context({"request": request}),
                    language=language,
                    use_cache=True,
                )
            if request.GET.get("html", False):
                html = render_html(request, placeholder, language)
                for key, value in html.items():
                    if not hasattr(placeholder, key):
                        setattr(placeholder, key, value)
                        self.fields[key] = serializers.CharField()
            placeholder.label = placeholder.get_label()
            placeholder.language = language
            self.instance = placeholder


class PlaceholderRelationSerializer(serializers.Serializer):
    content_type_id = serializers.IntegerField()
    object_id = serializers.IntegerField()
    slot = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
