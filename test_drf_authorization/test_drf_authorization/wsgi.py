import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'test_drf_authorization.settings')

application = get_wsgi_application()
