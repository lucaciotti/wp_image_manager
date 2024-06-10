from peewee import *
from ..base import BaseModel


class WpProduct(BaseModel):
    sku = CharField(unique=True)
    name = CharField(null=True)
    description = TextField(null=True)
    short_description = TextField(null=True)
    slug = CharField(null=True)
    regular_price = FloatField(default=0)
    image_name = CharField(null=True)
    image_WooId = IntegerField(null=True)
    image_DbId = IntegerField(null=True)
    no_image = BooleanField(default=False)
    category = CharField(null=True)
    category_WooId = IntegerField(null=True)
    category_DbId = IntegerField(null=True)
    status = CharField(null=True)
    button_text = CharField(null=True)
    weight = FloatField(null=True)
    dimension_length = FloatField(null=True)
    dimension_width = FloatField(null=True)
    dimension_height = FloatField(null=True)
    purchase_note = TextField(null=True)
    woocommerce_id = IntegerField(null=True)
    upload_to_site = BooleanField(default=False)
    pa_udm = CharField(null=True)
