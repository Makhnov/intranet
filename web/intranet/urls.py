from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from search import views as search_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_pdf_view import urls as wagtailpdf_urls
# from wagtail_content_import import urls as wagtailimport_urls

from .api import api_router
from users.views import UserPermissionDetailsView, CustomUserIndexView, profile_view
from administration.views import administration_search
from accompte.views import CustomPasswordChangeView
from agents.views import faq_filter, faq_search
from django.urls import path

urlpatterns = [
    path("api/v2/auth/", UserPermissionDetailsView.as_view(), name="auth"),
    path("api/v2/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v2/", include("dj_rest_auth.urls")),
    path("api/v2/", api_router.urls),
    path("django-admin/", admin.site.urls),
    path('admin/users/', CustomUserIndexView.as_view(), name='wagtailusers_users'),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("faq_filter/", faq_filter, name="faq_filter"),
    path("faq_search/", faq_search, name="faq_search"),
    path("administration/search/", administration_search, name="administration_search"),
    path('pdf/', include(wagtailpdf_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Note that this only works in development mode (DEBUG = True);
    # in production, you will need to configure your web server to serve files from MEDIA_ROOT.
    # For further details [...] extrait de https://github.com/torchbox/wagtailmedia#url-configuration

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path('account/password/change/', CustomPasswordChangeView.as_view(), name='account_password_change'),
    path("account/", include("allauth.urls")),
    path("account/profile/", profile_view, name="account_profile"),
    # path('', include(wagtailimport_urls)),
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    # path("pages/", include(wagtail_urls)),
]
