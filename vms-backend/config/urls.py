"""Root URLconf.

Phase 1b: admin auth, visitor CRUD, device pairing, scans and the screen feed.
The websocket route lands in phase 2 and is registered in `config/asgi.py`, not
here — `/ws/screen/` is not an HTTP path.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/", include("apps.common.urls")),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.visitors.urls")),
    path("api/v1/", include("apps.devices.urls")),
    path("api/v1/", include("apps.scans.urls")),
    path("api/v1/", include("apps.badges.urls")),
    path("api/v1/", include("apps.reports.urls")),
    path("api/v1/", include("apps.registrations.urls")),
    path("api/v1/", include("apps.assistant.urls")),
    # The walk-in desk: paired like a device, no login. Two routes only.
    path("api/v1/desk/", include("apps.desk.urls")),
    # Everything reachable without a token, on a router of its own.
    path("api/v1/public/", include("apps.registrations.public_urls")),
]

if settings.DEBUG:
    # Visitor photos over the dev server. Production serves them through the
    # signed-URL storage in apps/common — never a public /media/ directory.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
