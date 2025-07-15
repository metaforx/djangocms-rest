from functools import cached_property

from cms.app_base import CMSAppConfig


class RESTToolbarMixin:
    """
    Mixin to add REST rendering capabilities to the CMS toolbar.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def content_renderer(self):
        from .plugin_rendering import RESTRenderer

        return RESTRenderer(request=self.request)


class VersioningCMSConfig(CMSAppConfig):
    cms_enabled = True
    cms_toolbar_mixin = RESTToolbarMixin
