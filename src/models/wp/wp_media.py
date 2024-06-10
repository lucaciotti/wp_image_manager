from peewee import *
from ..base import BaseModel


class WpMedia(BaseModel):
    slug = CharField(unique=True)
    link = CharField(null=True)
    date = DateTimeField(null=True)
    woocommerce_id = IntegerField(null=True)
    upload_to_site = BooleanField(default=False)
