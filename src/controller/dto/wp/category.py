from .base import WpBaseDTO
from src.models import wp as m


class WpCategoryDTO(WpBaseDTO):
    name = None
    parent = None

    model_cls = m.WpCategory
    woo_instance = 'products/categories'

    def __init__(self, name_code, parent_code, **kwargs):
        self.name = name_code
        self.parent = parent_code
        
        self.db_id, self.woocommerce_id = self._dbExist()
        if self.woocommerce_id == None:
            # Se non c'è woocommerce_id vuol dire che deve essere creato online, a meno che non arrivi proprio da online
            self.woocommerce_id = kwargs['id'] if 'id' in kwargs else None
        
        self._buildDataDb()
        self._buildDataWooApi()

    def _dbExist(self):
        try:
            if self.parent is not None:
                record = self.model_cls.filter(name=self.name, parent=self.parent).get()
            else:
                record = self.model_cls.filter(name=self.name).get()
            if record and not isinstance(record, list):
                self.parent = record.parent
                return record.id, record.woocommerce_id
            else:
                return None, None
        except self.model_cls.DoesNotExist:
            return None, None
    
    def _buildDataDb(self):
        data = {
            'name': self.name,
        }
        data['parent'] = self.parent
        if self.woocommerce_id != None:
           data['woocommerce_id'] = self.woocommerce_id

        self.data_db = data

    def _buildDataWooApi(self):
        data = {
            'name': self.name,
        }
        data['parent'] = self.parent
        if self.woocommerce_id != None:
           data['id'] = self.woocommerce_id

        self.data_wooApi = data

    @classmethod
    def findCategoryByWooID(self, category_WooId):
        # Interrogo semplicemente il Database che mi restituisce le informazioni che mi servono
        try:
            cat = self.model_cls.filter(woocommerce_id=category_WooId).get()
            if cat is not None:
                return cat
        except self.model_cls.DoesNotExist:
            return None

    @classmethod
    def findCategoryByName(self, cat_name, prev_cat_name=None, create=True):
        # in questo caso costruisco un DTO e vedo se esiste altrimenti lo creo
        parent_id = None
        if prev_cat_name is not None:
            prevCat = self.model_cls.filter(name=prev_cat_name).get()
            if prevCat is not None:
                parent_id = prevCat.woocommerce_id

        cat = self(cat_name, parent_id)
        if cat.exist():
            return cat
        else:
            if create:
                # Creo la categoria!!
                cat.dto2WooApi()
                return cat
            else:
                return None