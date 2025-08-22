from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


@toolbar_pool.register
class RestToolbar(CMSToolbar):
    class Media:
        css = {"all": ("djangocms_rest/highlight.css",)}
