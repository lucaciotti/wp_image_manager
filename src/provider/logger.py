import logging

import typer

from src.provider.base import Singleton
from src.provider.config import Config
from src.provider.storage import RepoStorage
from src.provider.typerHandler import TyperCmdHandler, TyperLoggerHandler

class Logger(metaclass=Singleton):

    def __init__(self):
        config = Config()
        self.repoStorage = RepoStorage()
        self.typerCmdHandler = TyperCmdHandler()
        
        self.log_level = config.get_conf('log', 'level')
        self.log_stream_level = config.get_conf('log', 'stream_level')
        if not self.log_stream_level:
            self.log_stream_level = self.log_level

        self.path = self.repoStorage.getOrCreateSubPath('LOG')
        self.file = self.repoStorage.getFile(self.path, 'log.log')

        # Create a custom logger
        self.logger = logging.getLogger(__name__)

        # Create handlers
        if config.get_conf('log', 'typer')=='true':
            self.typer_handler = TyperLoggerHandler()
            self.typer_handler.setLevel(self.log_stream_level)
        else:
            self.c_handler = logging.StreamHandler()
            self.c_handler.setLevel(self.log_stream_level)
        self.f_handler = logging.FileHandler(self.file)
        self.f_handler.setLevel(self.log_level)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(levelname)s - %(message)s')
        if config.get_conf('log', 'typer')=='true':
            self.typer_handler.setFormatter(c_format)
        else:
            self.c_handler.setFormatter(c_format)
        f_format = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        self.f_handler.setFormatter(f_format)

        # Add handlers to the logger
        if config.get_conf('log', 'typer')=='true':
            self.logger.addHandler(self.typer_handler)
        else:
            self.logger.addHandler(self.c_handler)
        self.logger.addHandler(self.f_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def exeptionLog(self, message):
        self.logger.error(f"Exception: {message}", exc_info=True)

    def criticalExpLog(self, message):
        self.logger.critical(f"Exception Critical: {message}", exc_info=True)
        self.typerCmdHandler.abort()

    def archiveLog(self):
        self.logger.removeHandler(self.f_handler)
        self.f_handler.close()
        self.repoStorage.archiveFile('LOG', self.file, move=True)
