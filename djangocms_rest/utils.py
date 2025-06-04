from typing import Optional, Union

from cms.models import Page, PageUrl
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404


def get_object(site: Site, path: str) -> Page:
    page_urls = (
        PageUrl.objects.get_for_site(site).filter(path=path).select_related("page")
    )
    page_urls = list(page_urls)
    try:
        page = page_urls[0].page
    except IndexError:
        raise Http404
    else:
        page.urls_cache = {url.language: url for url in page_urls}
    return page


def get_absolute_frontend_url(path: str, site_id: Union[Site, int, str] = 1, protocol: Optional[str] = None) -> str:
    """
    Converts a relative path to an absolute URL using the site's domain.

    Args:
        path: The relative path to convert
        site_id: The ID of the site or a Site object
        protocol: The protocol to use (default is "https")

    Returns:
        A properly formatted absolute URL
    """
    # Return the original path if it's already an absolute URL
    if path.startswith(("http://", "https://")):
        return path

    site = Site.objects.get(id=int(site_id))
    domain = site.domain

    # Handle start/end slashes for domain and path
    if domain.endswith("/") and path.startswith("/"):
        domain = domain.rstrip("/")
    elif not domain.endswith("/") and not path.startswith("/"):
        domain = f"{domain}/"

    if protocol is None:
        protocol = getattr(settings, "FRONTEND_PROTOCOL", "https")

    return f"{protocol}://{domain}{path}"
