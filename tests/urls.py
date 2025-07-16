from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    path(
        "api/",
        include("djangocms_rest.urls"),
    ),
    path(
        "api/pizza/<int:pk>/", lambda request, pk: f"<Pizza: {pk}>", name="pizza-detail"
    ),
    path("admin/", admin.site.urls),
    path("", include("cms.urls")),
]

urlpatterns += staticfiles_urlpatterns()
