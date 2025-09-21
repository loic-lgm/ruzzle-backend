"""
WSGI config for ruzzle project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.getenv("ENV", "dev").lower()
if env == "prod":
    settings_module = "ruzzle_backend.settings_prod"
else:
    settings_module = "ruzzle_backend.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()
