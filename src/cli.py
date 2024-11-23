import sys
import typer
# from notifypy import Notify
from typing import Optional
from pathlib import Path

from src import __app_name__, __version__
from src.__main__ import CSVLOGGER
from src.controller.images_controller import ImagesController
from src.controller.main_controller import MainController
from src.controller.sync_db_controller import SyncLocalDBController
from src.provider.config import Config
# from src.models import fatturaEl as m
# from src.provider.notifier import Notifier
from src.provider.storage import RepoStorage
from src.provider.xmlReader import XmlReader

app = typer.Typer()
    
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        is_eager=True,
    ),
    noverbose: Optional[bool] = typer.Option(
        False,
        "--no-verbose",
        "-nv",
        help="Print the result of command",
    ),
    nointeractive: Optional[bool] = typer.Option(
        False,
        "--no-interactive",
        "-ni",
        help="Ask for each operation",
    ),
) -> None:
    """
    Manage users in the awesome CLI app.
    """
    params = ctx.ensure_object(dict)
    params["noverbose"] = noverbose
    params["nointeractive"] = nointeractive
    if ctx.invoked_subcommand is None:
        ctrl = MainController(ctx)
        ctrl.version_callback(version)
        ctrl.close()

@app.command()
def test(
    ctx: typer.Context,
    config: Optional[bool] = typer.Option(
        None,
        "--config",
        "-c",
        help="Check the application's config files.",
        # callback=_config_check,
        is_eager=True,
    ),
    notify: Optional[bool] = typer.Option(
        None,
        "--notify",
        "-n",
        help="Check Notification.",
        # callback=_notification_test,
        is_eager=True,
    ),
    db: Optional[bool] = typer.Option(
        None,
        "--DB",
        "-d",
        help="Check Database.",
        # callback=_init_db,
        is_eager=True,
    )
)-> None:
    ctrl = MainController(ctx)
    ctrl.check_config(config)
    ctrl.check_notification(notify)
    ctrl.check_db(db)
    ctrl.close()

@app.command()
def syncDataFromWp(
    product: Optional[bool] = typer.Option(
        None,
        "--product",
        "-p",
        help="Sync Product DB",
    ),
    category: Optional[bool] = typer.Option(
        None,
        "--category",
        "-c",
        help="Sync Categories DB",
    ),
    attribute: Optional[bool] = typer.Option(
        None,
        "--attribute",
        "-a",
        help="Sync Attributes DB",
    ),
    media: Optional[bool] = typer.Option(
        None,
        "--media",
        "-m",
        help="Sync Media DB",
    ),
) -> None:
    """Sync Data From Woocommerce."""
    ctrl=SyncLocalDBController(state['interactive'], verbose)
    if media:
        ctrl.syncMediaTable()
    if attribute:
        ctrl.syncAttributeTable()
    if category:
        ctrl.syncCategoryTable()
    if product:
        ctrl.syncProductTable()
    if not media and not attribute and not category and not product:
        ctrl.syncAllTables()
    ctrl.close()

@app.command()
def processImages(
    dir_path: Optional[str] = typer.Option(
        None,
        "--xml_dir_path",
        "-d"
    ),
    verbose: Optional[bool] = typer.Option(
        None,
        "--verbose",
        "-v",
        help="Print the result of command",
    ),
    skip_ct_filter: Optional[bool] = typer.Option(
        False,
        "--skip_ct_filter",
        "-s",
        help="Force reload all dir files",
    ),
) -> None:
    ImagesController().processImages()
    
    input("Press Enter to exit...")
    # CSVLOGGER.write_csv_rows()
    # CSVLOGGER.moveFile()
    raise typer.Exit()
