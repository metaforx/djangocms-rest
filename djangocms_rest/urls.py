from django.urls import path

from djangocms_rest.views import (
    LanguageListView,
    PageDetailView,
    PageListView,
    PageTreeListView,
    PlaceholderDetailView,
    PreviewPageView,
    PreviewPlaceholderDetailView,
    PreviewPageTreeListView,
    PreviewPageListView,
)

urlpatterns = [
    # Published content endpoints
    path(
        "languages/",
        LanguageListView.as_view(),
        name="language-list",
    ),
    path(
        "<slug:language>/pages-tree/",
        PageTreeListView.as_view(),
        name="page-tree-list",
    ),
    path(
        "<slug:language>/pages-list/",
        PageListView.as_view(),
        name="page-list",
    ),
    path(
        "<slug:language>/pages-root/",
        PageDetailView.as_view(),
        name="page-root",
    ),
    path(
        "<slug:language>/pages/<path:path>/",
        PageDetailView.as_view(),
        name="page-detail",
    ),
    path(
        "<slug:language>/placeholders/<int:content_type_id>/<int:object_id>/<str:slot>/",
        PlaceholderDetailView.as_view(),
        name="placeholder-detail",
    ),

    # Preview content endpoints
    path(
        "preview/<slug:language>/pages-root/",
        PreviewPageView.as_view(),
        name="preview-page-root",
    ),
    path(
        "preview/<slug:language>/pages-tree/",
        PreviewPageTreeListView.as_view(),
        name="preview-page-tree",
    ),
    path(
        "preview/<slug:language>/pages-list/",
        PreviewPageListView.as_view(),
        name="preview-page-list",
    ),
    path(
        "preview/<slug:language>/pages/<path:path>/",
        PreviewPageView.as_view(),
        name="preview-page",
    ),
    path(
        "preview/<slug:language>/placeholders/<int:content_type_id>/<int:object_id>/<str:slot>/",
        PreviewPlaceholderDetailView.as_view(),
        name="preview-placeholder-detail",
    ),
]
