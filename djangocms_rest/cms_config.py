from functools import cached_property

from django.conf import settings
from django.urls import NoReverseMatch, reverse

from cms.app_base import CMSAppConfig
from cms.models import Page
from cms.utils.i18n import force_language, get_current_language


try:
    from filer.models import File
except ImportError:
    File = None


def get_page_api_endpoint(page, language=None, fallback=True):
    """Get the API endpoint for a given page in a specific language.
    If the page is a home page, return the root endpoint.
    """
    if not language:
        language = get_current_language()

    with force_language(language):
        try:
            if page.is_home:
                return reverse("page-root", kwargs={"language": language})
            path = page.get_path(language, fallback)
            return (
                reverse("page-detail", kwargs={"language": language, "path": path})
                if path
                else None
            )
        except NoReverseMatch:
            return None


def get_file_api_endpoint(file):
    """For a file reference, return the URL of the file if it is public."""
    if not file:
        return None
    return file.url if file.is_public else None


class RESTToolbarMixin:
    """
    Mixin to add REST rendering capabilities to the CMS toolbar.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if getattr(
        settings, "REST_JSON_RENDERING", not getattr(settings, "CMS_TEMPLATES", False)
    ):
        try:
            from djangocms_text import settings

            settings.TEXT_INLINE_EDITING = False
        except ImportError:
            pass

        @cached_property
        def content_renderer(self):
            from .plugin_rendering import RESTRenderer

            return RESTRenderer(request=self.request)


class RESTCMSConfig(CMSAppConfig):
    cms_enabled = True
    cms_toolbar_mixin = RESTToolbarMixin

    Page.add_to_class("get_api_endpoint", get_page_api_endpoint)
    File.add_to_class("get_api_endpoint", get_file_api_endpoint) if File else None
