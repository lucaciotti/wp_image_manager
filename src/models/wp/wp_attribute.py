from peewee import *
from ..base import BaseModel


class WpAttribute(BaseModel):
    name = CharField(null=True)
    slug = CharField(null=True)
    type = CharField(null=True)
    woocommerce_id = IntegerField(null=True)
    upload_to_site = BooleanField(default=False)

    class Meta:
        indexes = (
            (('name',), True),
        )


class WpAttributeValue(BaseModel):
    name = CharField(null=True)
    slug = CharField(null=True)
    description = CharField(null=True)
    woocommerce_id = IntegerField(null=True)
    attribute_WooId = IntegerField(null=True)
    attribute_DbId = IntegerField(null=True)
    upload_to_site = BooleanField(default=False)

    class Meta:
        indexes = (
            (('name',), True),
        )
