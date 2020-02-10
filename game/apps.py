from django.apps import AppConfig
from . import scheduler
from .postgrehelper import PostgreHelp
GLOBALSCHEDULE = None
class GameConfig(AppConfig):
    name = 'game'

    def ready(self):             
        scheduler.start()
        postgreHelp = PostgreHelp()
        postgreHelp.TruncateTables()
