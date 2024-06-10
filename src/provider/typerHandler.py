import logging
import typer

from src.provider.base import Singleton


class TyperLoggerHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:
        fg = None
        bg = None
        if record.levelno == logging.DEBUG:
            fg = typer.colors.BLACK
        elif record.levelno == logging.INFO:
            fg = typer.colors.BRIGHT_BLUE
        elif record.levelno == logging.WARNING:
            fg = typer.colors.BRIGHT_MAGENTA
        elif record.levelno == logging.ERROR:
            fg = typer.colors.BRIGHT_RED
        elif record.levelno == logging.CRITICAL:
            fg = typer.colors.BRIGHT_WHITE
            bg = typer.colors.RED
        typer.secho(self.format(record), bg=bg, fg=fg)


class TyperCmdHandler(metaclass=Singleton):

    def __init__(self, verbose=True, interactive=True):
        self.verbose = verbose
        self.interactive = interactive

    def setVerbose(self, verbose):
        self.verbose = verbose

    def setInteractive(self, interactive):
        self.interactive = interactive
        
    def echo(self, message):
        if self.verbose:
            typer.secho(message=message)

    def echoGreen(self, message):
        if self.verbose:
            typer.secho(message=message, fg=typer.colors.GREEN)
    
    def echoYellow(self, message):
        if self.verbose:
            typer.secho(message=message, fg=typer.colors.YELLOW)
    
    def echoRed(self, message):
        if self.verbose:
            typer.secho(message=message, fg=typer.colors.RED)

    def input(self, message, default_val=None):
        if self.interactive:
            return typer.prompt(message, default=default_val)
    
    def confirm(self, message, default_val=None):
        if self.interactive:
            return typer.confirm(message, default=default_val)

    def confirmEnter(self, message="Press Enter to exit...", default_val=True):
        if self.interactive:
            return typer.confirm(message, default=default_val, prompt_suffix='', show_default=False)
        
    def abort(self):
        raise typer.Abort()
        
    def exit(self):
        raise typer.Exit()