from cms.models import Page, PageContent, Placeholder
from cms.utils.conf import get_languages
from cms.utils.page_permissions import user_can_view_page
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.response import Response

from djangocms_rest.permissions import CanViewPage, CanViewPageContent, IsAllowedLanguage
from djangocms_rest.serializers.languages import LanguageSerializer
from djangocms_rest.serializers.pages import PageContentSerializer, PageMetaSerializer, PreviewPageContentSerializer
from djangocms_rest.serializers.placeholders import PlaceholderSerializer
from djangocms_rest.utils import get_object, get_placeholder
from djangocms_rest.views_base import BaseAPIView
from rest_framework.permissions import IsAdminUser


class LanguageListView(BaseAPIView):
    serializer_class = LanguageSerializer

    def get(self, request: Request | None) -> Response:
        """List of languages available for the site. For each language the API returns the
        link to the list of pages for that languages."""
        languages = get_languages().get(get_current_site(request).id, None)
        if languages is None:
            raise Http404
        for conf in languages:
            conf["pages"] = f"{request.scheme}://{request.get_host()}" + reverse("page-tree-list", args=(conf["code"],))
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)


class PageTreeListView(BaseAPIView):
    permission_classes = [IsAllowedLanguage]
    serializer_class = PageMetaSerializer

    def get(self, request, language):
        """List of all pages on this site for a given language."""
        site = self.site
        qs = Page.objects.filter(node__site=site)
        if request.user.is_anonymous:
            qs = qs.filter(login_required=False)
        pages = (
            page.get_content_obj(language, fallback=True)
            for page in qs
            if user_can_view_page(request.user, page) and page.get_content_obj(language, fallback=True)
        )
        serializer = PageMetaSerializer(
            pages,
            many=True,
            read_only=True,
        )
        return Response(serializer.data)


class PageDetailView(BaseAPIView):
    permission_classes = [CanViewPage]
    serializer_class = PageContentSerializer

    def get(self, request: Request, language: str, path: str = "") -> Response:
        """Retrieve a page instance. The page instance includes the placeholders and
        their links to retrieve dynamic content."""
        site = self.site
        page = get_object(site, path)
        self.check_object_permissions(request, page)
        page_content = page.get_content_obj(language, fallback=True)
        serializer = PageContentSerializer(page_content, read_only=True)
        try:
            data = serializer.data
        except PageContent.DoesNotExist:
            raise Http404
        return Response(data)


class PlaceholderDetailView(BaseAPIView):
    serializer_class = PlaceholderSerializer
    permission_classes = [CanViewPageContent]

    def get(self, request: Request, language: str, content_type_id: int, object_id: int, slot: str) -> Response:
        """Placeholder contain the dynamic content. This view retrieves the content as a
        structured nested object.

        Attributes:
        - "slot": The slot name of the placeholder.
        - "content": The content of the placeholder as a nested JSON tree
        - "language": The language of the content
        - "label": The verbose label of the placeholder

        Optional (if the get parameter `?html=1` is added to the API url):
        - "html": The content rendered as html. Sekizai blocks such as "js" or "css" will be added
          as separate attributes"""
        placeholder = get_placeholder(content_type_id, object_id, slot)
        if placeholder is None:
            raise Http404

        source = placeholder.content_type.model_class().objects.filter(pk=placeholder.object_id).first()
        if source is None:
            raise Http404

        self.check_object_permissions(request, source)

        serializer = self.serializer_class(instance=placeholder, request=request, language=language, read_only=True)
        return Response(serializer.data)

#NOTE: This is working, but might need refactoring
class PreviewPlaceholderDetailView(BaseAPIView):
    serializer_class = PlaceholderSerializer
    permission_classes = [IsAdminUser, CanViewPage]

    def get(self, request: Request, language: str, content_type_id: int, object_id: int, slot: str) -> Response:
        """Placeholder contain the dynamic content. This view retrieves the content as a
        structured nested object.
        """
        try:
            placeholder = Placeholder.objects.get(
                content_type_id=content_type_id, object_id=object_id, slot=slot
            )
        except Placeholder.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(
            instance=placeholder, 
            request=request, 
            language=language, 
            read_only=True
        )
        return Response(serializer.data)

#NOTE: This is working, but might need refactoring
class PreviewPageView(BaseAPIView):
    """View for previewing unpublished page content"""
    permission_classes = [IsAdminUser, CanViewPage]
    serializer_class = PreviewPageContentSerializer 

    def get(self, request: Request, language: str, path: str = "") -> Response:
        """Retrieve a draft/preview version of a page instance."""
        site = self.site
        page = get_object(site, path)
        self.check_object_permissions(request, page)
        
        try:
            # Get all draft versions for this page and language
            all_page_contents = PageContent.admin_manager.filter(
                page=page,
                language=language
            ).order_by('-creation_date')
            
            # Get the latest draft version
            page_content = all_page_contents.first()
            
            if not page_content:
                raise PageContent.DoesNotExist
            
            # Use our new serializer with proper context
            serializer = PreviewPageContentSerializer(
                page_content, 
                read_only=True,
                context={'request': request}
            )
            
            return Response(serializer.data)
        except PageContent.DoesNotExist:
            raise Http404
            
#NOTE: This is working, but might need refactoring
class PreviewPageTreeListView(BaseAPIView):
    permission_classes = [IsAdminUser, IsAllowedLanguage]
    serializer_class = PageMetaSerializer

    def get(self, request, language):
        """List of all draft/preview pages on this site for a given language."""
        site = self.site
        qs = Page.objects.filter(node__site=site)
        
        # Create a generator similar to PageTreeListView but using admin_manager
        pages = (
            PageContent.admin_manager.filter(
                page=page,
                language=language
            ).order_by('-creation_date').first() or page.get_content_obj(language, fallback=True)
            for page in qs
            if user_can_view_page(request.user, page)
        )
        
        # Filter out None values
        pages = [page for page in pages if page]
        
        serializer = PageMetaSerializer(
            pages,
            many=True,
            read_only=True,
        )
        return Response(serializer.data)
