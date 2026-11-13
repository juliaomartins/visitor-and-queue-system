"""Settings for the test suite. SQLite, never the event's Postgres.

    ..\\.venv\\Scripts\\python.exe manage.py test apps.assistant --settings=config.settings.test

CLAUDE.md records why this is a settings module and not a runtime swap: a
probe that rewrote `connections.databases` after Django had read its
configuration wrote visitors and scans into the live event database. Django's
test runner builds its own database from whatever this names -- for SQLite an
in-memory one -- so nothing here can reach Postgres.
"""

import tempfile
from pathlib import Path

from .dev import *  # noqa: F401,F403
from .dev import BASE_DIR

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}

# No test may reach OpenAI. Tests that need a model pass a fake one.
OPENAI_API_KEY = ""

# Hashing with the real hasher is most of the time a user-creating test takes.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

MEDIA_ROOT = Path(tempfile.gettempdir()) / "vms-test-media"
