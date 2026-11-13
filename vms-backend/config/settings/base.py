"""Shared settings for every environment.

The backend runs as ONE process under uvicorn/daphne — see CLAUDE.md, hard
constraint #1. `InMemoryChannelLayer` keeps group membership in a per-process
dict, so multiple workers silently break the lobby screen.
"""

from datetime import timedelta
from pathlib import Path

import environ

from apps.common.network import default_media_base_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, ["*"]),
    POSTGRES_DB=(str, "vms"),
    POSTGRES_USER=(str, "vms"),
    POSTGRES_PASSWORD=(str, "vms"),
    POSTGRES_HOST=(str, "127.0.0.1"),
    POSTGRES_PORT=(int, 5432),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-insecure-change-me")

# Badge QR tokens are an HMAC under this secret, so it decides which printed
# cards are valid. Deliberately NOT SECRET_KEY: rotating Django's key is routine
# and must not void 250 printed badges. Changing this value invalidates every
# badge already in circulation.
BADGE_TOKEN_SECRET = env("VMS_BADGE_TOKEN_SECRET", default=SECRET_KEY)
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")

# --------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------

INSTALLED_APPS = [
    "daphne",  # MUST stay first, before staticfiles
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "apps.common",
    "apps.accounts",
    "apps.visitors",
    "apps.badges",
    "apps.devices",
    "apps.scans",
    "apps.reports",
    "apps.registrations",
    "apps.desk",
    "apps.assistant",
]

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    # FIRST, and the position is the whole point: response middleware runs
    # bottom-to-top, so sitting at the top means this compresses AFTER every
    # other middleware has finished writing the body -- including the CORS
    # headers below it.
    #
    # The visitor list is 82 KB of JSON at 250 visitors and 14 KB gzipped, and
    # the print queue's `?with_tokens=true` is 102 KB down to 25 KB. Both are
    # admin calls; the scan path the door depends on is a small POST and is not
    # affected.
    #
    # Not the BREACH worry it would be on a public site: these responses carry
    # no CSRF token, the dashboard is same-origin through its own proxy, and an
    # attacker who could measure compressed sizes on this closed LAN already
    # has the admin's bearer token. Revisit if this API is ever exposed.
    "django.middleware.gzip.GZipMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"  # manage.py only
ASGI_APPLICATION = "config.asgi.application"  # THE entry point

# --------------------------------------------------------------------------
# Channels — no Redis, deliberately (CLAUDE.md hard constraint #2)
# --------------------------------------------------------------------------

CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
}

# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------------
# i18n / static / media
# --------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
# The event runs in Timor-Leste. Storage stays UTC (USE_TZ is on); this is what
# the server GROUPS and PRESENTS in, and getting it wrong is silent: hourly
# arrival buckets would be nine hours out and "today" would start at 09:00.
TIME_ZONE = env("VMS_TIME_ZONE", default="Asia/Dili")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Absolute origin for visitor photos. The lobby screen and the guard's phone are
# other machines, so a relative URL would resolve against THEIR origin and 404.
# Building from a fixed base rather than the request also keeps the WebSocket push
# and the /screen/feed backfill byte-identical — the WS path has no request to
# build from.
#
# Detected, not hardcoded: this address is DHCP unless someone reserved it, and a
# stale value here fails silently as missing photos on every device at once. Set
# VMS_MEDIA_BASE_URL explicitly only when the guess is wrong — several NICs, a VPN
# adapter, or a reverse proxy in front.
MEDIA_BASE_URL = env("VMS_MEDIA_BASE_URL", default=default_media_base_url())

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------
# DRF + simplejwt + spectacular
# --------------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_THROTTLE_RATES": {
        "scans": "30/min",  # a real guard does ~10
        # FAILED pairing attempts per IP; a success clears the count. Every device
        # at the event shares the router's address, so this budget is shared —
        # which is why it counts only failures and why it is not 5.
        "pairing": "20/hour",
        # Public self-registration. Every POST counts, per client address and in
        # total -- see apps/registrations/throttling.py for why there are two.
        "public_registration": "10/hour",
        "public_registration_global": "200/hour",
        "public_status": "60/min",
        # The walk-in desk, per paired device. Far above a real desk's pace and
        # low enough that a stolen token cannot fill the roster unnoticed.
        "desk_registration": "120/hour",
        "desk_qr": "600/hour",
        # The dashboard's chat assistant, per admin. Each question is one or more
        # paid OpenAI calls; a person typing does a few a minute.
        "assistant": "20/min",
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# The dashboard keeps the access token in memory and never touches the refresh
# token: it lives in an httpOnly cookie set by the auth views. localStorage is
# out of the question — this app holds every visitor's photo.
REFRESH_COOKIE = {
    "NAME": env("VMS_REFRESH_COOKIE_NAME", default="vms_refresh"),
    # Scoped to the auth routes, so the cookie is not attached to every request.
    "PATH": "/api/v1/auth",
    "SAMESITE": "Lax",
    # The LAN is http:// (constraint #9); a Secure cookie would never be sent.
    "SECURE": env.bool("VMS_REFRESH_COOKIE_SECURE", default=False),
}

# --------------------------------------------------------------------------
# Devices and scans
# --------------------------------------------------------------------------

# A pairing code is typed in while an admin stands next to the device. Long
# enough to walk across the room, short enough that a photographed dashboard
# stops being useful.
DEVICE_PAIRING_CODE_TTL = timedelta(
    minutes=env.int("VMS_PAIRING_CODE_TTL_MINUTES", default=15)
)

# A visitor rescanned inside this window is logged as `duplicate` and kept off
# the lobby screen — a guard re-presenting a badge must not restart the welcome.
SCAN_DUPLICATE_WINDOW = timedelta(
    seconds=env.int("VMS_SCAN_DUPLICATE_WINDOW_SECONDS", default=60)
)

# Ceiling on one backfill response. A screen that has been down for an hour
# catches up over a few polls rather than in one enormous payload.
SCREEN_FEED_MAX_EVENTS = env.int("VMS_SCREEN_FEED_MAX_EVENTS", default=50)

# --------------------------------------------------------------------------
# Logging — `vms.audit` carries every admin write against a Visitor
# --------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "audit": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "audit"},
    },
    "loggers": {
        "vms.audit": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

# --------------------------------------------------------------------------
# Chat assistant — see apps/assistant
# --------------------------------------------------------------------------

# Empty disables the assistant; the dashboard says so instead of failing. With a
# key set, this server needs internet access, and the visitor rows the assistant
# retrieves (names, countries, organisations -- never photos or badge tokens)
# are sent to OpenAI to write each answer.
OPENAI_API_KEY = env("OPENAI_API_KEY", default="")
ASSISTANT_MODEL = env("VMS_ASSISTANT_MODEL", default="gpt-4o-mini")
ASSISTANT_TIMEOUT_SECONDS = env.int("VMS_ASSISTANT_TIMEOUT_SECONDS", default=60)

SPECTACULAR_SETTINGS = {
    "TITLE": "VMS API",
    "DESCRIPTION": "Visitor Management System — event badge scanning on a closed LAN.",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "COMPONENT_SPLIT_REQUEST": True,
    # UserSerializer has no endpoint yet; publish its component anyway.
    "POSTPROCESSING_HOOKS": [
        "apps.common.schema.register_phase0_components",
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
}
