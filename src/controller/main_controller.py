import sys
from src.controller.base import BaseController

from src import __app_name__, __version__

class MainController(BaseController):
    
    def version_callback(self, value: bool) -> None:
        if value:
            self.typerHandler.echo(f"{__app_name__} v{__version__}")
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                self.typerHandler.echo('running in a PyInstaller bundle')
            else:
                self.typerHandler.echo('running in a normal Python process')

    def check_config(self, value: bool) -> None:
        if value:
            dict_conf = self.config.dict_conf()
            self.typerHandler.echoGreen(f"The Config file contains: {dict_conf}")

    def check_notification(self, value: bool) -> None:
        if value:
            # Notifier().send('Prova', 'Prova eseguita con successo.')       
            pass
        
    def check_db(self, value: bool) -> None:
        if value:
            # doc = m.Doc
            pass