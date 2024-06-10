from .base import WpBaseDTO
from src.models import wp as m


class WpAttributeDTO(WpBaseDTO):
    name = None
    slug = None
    type = None

    model_cls = m.WpAttribute
    woo_instance = 'products/attributes'

    def __init__(self, slug_attr, **kwargs):
        self.slug = slug_attr

        self.name = kwargs['name'] if 'name' in kwargs else self.slug[3:].upper()
        self.type = kwargs['type'] if 'type' in kwargs else 'select'

        self.db_id, self.woocommerce_id = self._dbExist()
        if self.woocommerce_id == None:
            # Se non c'è woocommerce_id vuol dire che deve essere creato online, a meno che non arrivi proprio da online
            self.woocommerce_id = kwargs['id'] if 'id' in kwargs else None

        self._buildDataDb()
        self._buildDataWooApi()

    def _dbExist(self):
        try:
            record = self.model_cls.filter(slug=self.slug).get()
            if record:
                return record.id, record.woocommerce_id
            else:
                return None, None
        except self.model_cls.DoesNotExist:
            return None, None

    def _buildDataDb(self):
        data = {
            'name': self.name,
        }
        data['slug'] = self.slug
        data['type'] = self.type

        if self.woocommerce_id != None:
           data['woocommerce_id'] = self.woocommerce_id

        self.data_db = data

    def _buildDataWooApi(self):
        data = {
            'name': self.name,
        }
        data['slug'] = self.slug
        data['type'] = self.type
        if self.woocommerce_id != None:
           data['id'] = self.woocommerce_id

        self.data_wooApi = data


class WpAttributeValueDTO(WpBaseDTO):
    name = None
    slug = None
    description = None
    attribute_WooId = None
    attribute_DbId = None

    model_cls = m.WpAttributeValue
    woo_instance = 'products/attributes/{attribute_WooId}/terms'

    def __init__(self, slug_value, attribute_Woo_Id, attribute_Db_Id, **kwargs):
        self.slug = slug_value
        self.attribute_WooId = attribute_Woo_Id
        self.attribute_DbId = attribute_Db_Id

        self.name = kwargs['name'] if 'name' in kwargs else self.slug
        self.description = kwargs['description'] if 'description' in kwargs else self.slug

        self.db_id, self.woocommerce_id = self._dbExist()
        if self.woocommerce_id == None:
            # Se non c'è woocommerce_id vuol dire che deve essere creato online, a meno che non arrivi proprio da online
            self.woocommerce_id = kwargs['id'] if 'id' in kwargs else None

        self._buildDataDb()
        self._buildDataWooApi()

    def _dbExist(self):
        try:
            record = self.model_cls.filter(slug=self.slug).get()
            if record:
                return record.id, record.woocommerce_id
            else:
                return None, None
        except self.model_cls.DoesNotExist:
            if self.name != None:
                try:
                    record = self.model_cls.filter(name=self.name).get()
                    if record:
                        return record.id, record.woocommerce_id
                    else:
                        return None, None
                except self.model_cls.DoesNotExist:
                    if self.woocommerce_id != None:
                        try:
                            record = self.model_cls.filter(
                                woocommerce_id=self.woocommerce_id).get()
                            if record:
                                return record.id, record.woocommerce_id
                            else:
                                return None, None
                        except self.model_cls.DoesNotExist:
                            return None, None
            else:
                if self.woocommerce_id != None:
                    try:
                        record = self.model_cls.filter(
                            woocommerce_id=self.woocommerce_id).get()
                        if record:
                            return record.id, record.woocommerce_id
                        else:
                            return None, None
                    except self.model_cls.DoesNotExist:
                        return None, None
            return None, None

    def _buildDataDb(self):
        data = {
            'slug': self.slug,
        }
        data['name'] = self.name
        data['description'] = self.description
        data['attribute_WooId'] = self.attribute_WooId
        data['attribute_DbId'] = self.attribute_DbId

        if self.woocommerce_id != None:
           data['woocommerce_id'] = self.woocommerce_id

        self.data_db = data

    def _buildDataWooApi(self):
        data = {
            'slug': self.slug,
        }
        data['name'] = self.name
        data['description'] = self.description
        if self.woocommerce_id != None:
           data['id'] = self.woocommerce_id

        self.data_wooApi = data
