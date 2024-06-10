from peewee import *
import datetime

from src.models.base import BaseModel
from src.models.wp.wp_media import WpMedia


class LocalMedia(BaseModel):
    basename = CharField()
    category = CharField()
    filetype = CharField(null=True)
    path = CharField(null=True)
    relative_path = CharField(null=True)
    date_ct = DateTimeField(default=datetime.datetime.now)
    wp_media = ForeignKeyField(WpMedia, backref='docs')