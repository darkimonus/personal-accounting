from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# swagger
from rest_framework import permissions
from users import urls as users_urls
from incomes.urls import urlpatterns as incomes_urls

SchemaView = get_schema_view(
    openapi.Info(
        title="project Sample API",
        default_version="v1",
        description="DRF Swagger",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

auth_urlpatterns = [
    path("", include("oauth2_provider.urls", namespace="oauth2_provider")),
]
if settings.ENABLE_OAUTH:
    auth_urlpatterns += [
        re_path(r"^o/", include("drf_social_oauth2.urls", namespace="drf")),
        path("", include("social_django.urls", namespace="social")),
    ]

urlpatterns = [
    re_path(
        r"^doc(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "doc/",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        SchemaView.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path('admin/', admin.site.urls),
    path("auth/", include(auth_urlpatterns)),
    path('users/', include(users_urls)),
    path('income/', include(incomes_urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
