from .base import DBobj
from src.models import local as lm
from src.models import wp as wm

local_models = [lm.LocalMedia]
wp_models = [wm.WpProduct, wm.WpCategory, wm.WpAttribute, wm.WpAttributeValue, wm.WpMedia]

DBobj.syncModels(local_models)
DBobj.syncModels(wp_models)
