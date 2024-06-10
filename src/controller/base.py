from src.provider.config import Config
from src.provider.logger import Logger
from src.provider.storage import RepoStorage
from src.provider.typerHandler import TyperCmdHandler

class BaseController:   

    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.main_params = ctx.ensure_object(dict)
        self.config = Config()
        self.repoStorage = RepoStorage()
        self.logger = Logger()
        self.typerHandler = TyperCmdHandler()
        self.typerHandler.setInteractive(not self.main_params['nointeractive'])
        self.typerHandler.setVerbose(not self.main_params['noverbose'])
        # self.notification = Notifier()

    def close(self):
        self.typerHandler.confirmEnter()
        self.logger.archiveLog()
        self.typerHandler.exit()