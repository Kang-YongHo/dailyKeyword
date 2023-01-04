import os
from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'search'

    def ready(self):
        from . import updater
        if os.environ.get('RUN_MAIN'):
            updater.start()
