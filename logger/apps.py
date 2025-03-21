from django.apps import AppConfig
import threading
import os

class LoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logger'

    def ready(self):
        # Prevent multiple thread spawns in dev reloader
        if os.environ.get('RUN_MAIN', None) != 'true':
            return

        from biometrics_logging import start_biometrics_logger
        threading.Thread(target=start_biometrics_logger, daemon=True).start()
