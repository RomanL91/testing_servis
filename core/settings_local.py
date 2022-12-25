# from pathlib import Path
# import south

from .settings import BASE_DIR

# BASE_DIR = Path(__file__).resolve().parent.parent


ALLOWED_HOSTS = ["*"]
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# SOUTH_DATABASE_ADAPTERS = {
#     'default': 'south.db.sqlite3',
# }

# почему не environ?..
