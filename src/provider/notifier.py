
# from desktop_notify import Notify
# from src import __app_name__, __version__

class Notifier:
    notification = None

    def __init__(self):
        # self.notification = desktop_notify.aio.Server(f"{__app_name__} v{__version__}")
        pass

    def send(self, title, message):
        pass
        # self.notification.title = title
        # self.notification.message = message
        # self.notification.send()