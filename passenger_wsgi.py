import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

for path in (BASE_DIR, SRC_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BigBytes.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
