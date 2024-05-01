from django.apps import AppConfig
from .scheduler import start as start_scheduler

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    # def ready(self):
    #     print("✅ PyConsole Application is Ready!")
    #     start_scheduler()
 