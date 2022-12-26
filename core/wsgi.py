"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
from config import DEBUG

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = Cling(get_wsgi_application())

if DEBUG:
    from app.bot.update import updater
    updater.start_polling()