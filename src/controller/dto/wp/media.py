from .base import WpBaseDTO
from src.models import wp as m


class WpMediaDTO(WpBaseDTO):
    slug = None
    link = None
    date = None

    model_cls = m.WpMedia
    woo_instance = 'media'

    def __init__(self, slug_code, **kwargs):
        self.slug = slug_code
        self.link = kwargs['link'] if 'link' in kwargs else None
        self.date = kwargs['date'] if 'date' in kwargs else None

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
            try:
                record = self.model_cls.filter(slug=self.slug.lower()).get()
                if record:
                    return record.id, record.woocommerce_id
                else:
                    return None, None
            except self.model_cls.DoesNotExist:
                return None, None
    
    def _buildDataDb(self):
        data = {
            'slug': self.slug,
        }
        if self.link != None:
           data['link'] = self.link
        if self.date != None:
           data['date'] = self.date
        if self.woocommerce_id != None:
           data['woocommerce_id'] = self.woocommerce_id
        
        self.data_db = data

    def _buildDataWooApi(self):
        data = {
            'slug': self.slug,
        }
        if self.link != None:
           data['link'] = self.link
        if self.date != None:
           data['date'] = self.date
        if self.woocommerce_id != None:
           data['id'] = self.woocommerce_id

        self.data_wooApi = data
        
        
