from sekizai.context import SekizaiContext
from sekizai.helpers import get_varname


def render_html(request, placeholder, language):
    from cms.plugin_rendering import ContentRenderer

    content_renderer = ContentRenderer(request)
    context = SekizaiContext({"request": request, "LANGUAGE_CODE": language})
    content = content_renderer.render_placeholder(
        placeholder,
        context=context,
        language=language,
        use_cache=True,
    )
    sekizai_blocks = context[get_varname()]

    return {
        "html": content,
        **{key: "".join(value) for key, value in sekizai_blocks.items() if value},
    }
