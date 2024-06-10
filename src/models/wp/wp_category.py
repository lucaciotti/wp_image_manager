from peewee import *
from ..base import BaseModel


class WpCategory(BaseModel):
    name = CharField(null=True)
    parent = IntegerField(default=0)
    woocommerce_id = IntegerField(null=True)
    upload_to_site = BooleanField(default=False)

    class Meta:
        indexes = (
            (('name', 'parent'), True),
        )
