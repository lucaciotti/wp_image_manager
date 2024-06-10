from .base import WpBaseDTO
from src.models import wp as m
from .media import WpMediaDTO
from .category import WpCategoryDTO
from .attribute import WpAttributeDTO, WpAttributeValueDTO
from src.utils.txt_formatter import TxtFormatter


class WpProductDTO(WpBaseDTO):
    sku = None
    name = None
    description = None
    short_description = None
    slug = None
    regular_price = None
    image_name = '-'
    image_WooId = None
    image_DbId = None
    no_image = False
    category = None
    category_WooId = None
    category_DbId = None
    prevCategory = None
    prevCategory_WooId = None
    prevCategory_DbId = None
    status = None
    button_text = None
    weight = None
    dimension_length = None
    dimension_width = None
    dimension_height = None
    purchase_note = None
    attributes = []

    model_cls = m.WpProduct
    woo_instance = 'products'

    def __init__(self, sku_code, **kwargs):
        self.sku = sku_code
        if 'name' in kwargs:
            self.name = kwargs['name']
            self.slug = self.name.lower().replace(' ', '_')

        self.description = TxtFormatter.txtDescrFormat(kwargs['description'] if 'description' in kwargs else None)
        self.short_description = TxtFormatter.txtDescrFormat(kwargs['short_description'] if 'short_description' in kwargs else None)

        if 'images' in kwargs:
            #I dati mi arrivano da Woocommerce
            self.image_WooId = kwargs['images'][0]['id']
            self._findImageByWooID()
        else:
            #I dati mi arrivano da XLS o altro import
            if 'image_name' in kwargs:
                self.image_name = kwargs['image_name']
                self._findImageByName()
                self.image_name = kwargs['image_name']

        if 'categories' in kwargs:
            # I dati mi arrivano da Woocommerce
            self.category_WooId = kwargs['categories'][0]['id']
            self._findCategoryByWooID()
        else:
            # I dati mi arrivano da XLS o altro import
            if 'category_name' in kwargs:
                if '>' in kwargs['category_name']:
                    self.category = kwargs['category_name'][kwargs['category_name'].index('>')+1:].strip()
                    self.prevCategory = kwargs['category_name'][:kwargs['category_name'].index('>')].strip()
                    self._findCategoryByName()
                else:
                    self.category = kwargs['category_name'].strip()
                    self.prevCategory = None
                    self._findCategoryByName()
            
            if 'category_WooId' in kwargs:
                self.category_WooId = kwargs['category_WooId']
                self._findCategoryByWooID()

        if 'regular_price' in kwargs:
            try:
                self.regular_price = float(kwargs['regular_price'].replace(',', '.')) if type(kwargs['regular_price']) is str else kwargs['regular_price']
            except ValueError:
                self.regular_price = 0

        if 'status' in kwargs:
            if isinstance(kwargs['status'], bool):
                self.status = 'private' if kwargs['status'] == False else 'publish'
            elif isinstance(kwargs['status'], int):
                self.status = 'private' if kwargs['status'] == 0 else 'publish'
            elif isinstance(kwargs['status'], float):
                self.status = 'private' if kwargs['status'] == 0 else 'publish'
            else:
                self.status = kwargs['status']

        # self.weight = kwargs['weight'] if 'weight' in kwargs else None
        if 'weight' in kwargs:
            try:
                if isinstance(kwargs['weight'], bool):
                    self.weight = None
                elif isinstance(kwargs['weight'], int):
                    self.weight = float(kwargs['weight'])
                elif isinstance(kwargs['weight'], float):
                    self.weight = kwargs['weight']
                elif isinstance(kwargs['weight'], list):
                    self.weight = float(kwargs['weight'][0])
                else:
                    self.weight = float(kwargs['weight'])
            except Exception:
                self.weight = None

        if 'dimensions' in kwargs:
            # I dati mi arrivano da Woocommerce
            try:
                self.dimension_height = float(kwargs['dimensions']['height'])
            except ValueError:
                self.dimension_height = 0
            try:
                self.dimension_length = float(kwargs['dimensions']['length'])
            except ValueError:
                self.dimension_length = 0
            try:
                self.dimension_width = float(kwargs['dimensions']['width'])
            except ValueError:
                self.dimension_width = 0
        else:
            self.dimension_height = kwargs['dimension_height'] if 'dimension_height' in kwargs else None
            self.dimension_length = kwargs['dimension_length'] if 'dimension_length' in kwargs else None
            self.dimension_width = kwargs['dimension_width'] if 'dimension_width' in kwargs else None
        
        if 'attributes' in kwargs:
            if len(kwargs['attributes'])>0:
                for attr in kwargs['attributes']:
                    self._findAttributesByWooID(attr)

        # cerco un valore "pa_" in kwargs:
        for key in kwargs:
            if key.startswith('pa_'):
                if kwargs[key] is not None:
                    self._findAttributeByName(key, kwargs[key])
        
        self.button_text = kwargs['button_text'] if 'button_text' in kwargs else None
        self.purchase_note = kwargs['purchase_note'] if 'purchase_note' in kwargs else None

        self.db_id, self.woocommerce_id = self._dbExist()
        if self.woocommerce_id == None:
            # Se non c'è woocommerce_id vuol dire che deve essere creato online, a meno che non arrivi proprio da online
            self.woocommerce_id = kwargs['id'] if 'id' in kwargs else None

        self._buildDataDb()
        self._buildDataWooApi()
    
    def _dbExist(self):
        try:
            record = self.model_cls.filter(sku=self.sku).get()
            if record:
                return record.id, record.woocommerce_id
            else:
                return None, None
        except self.model_cls.DoesNotExist:
            return None, None

    def _buildDataWooApi(self):
        data = {
            'sku': self.sku,
        }
        if self.woocommerce_id != None:
           data['id'] = self.woocommerce_id
        if self.name != None:
           data['name'] = self.name
        if self.description != None:
           data['description'] = self.description
        if self.short_description != None:
           data['short_description'] = self.short_description
        if self.slug != None:
           data['slug'] = self.slug
        if self.regular_price != None:
           data['regular_price'] = str(self.regular_price)
        if self.category_WooId != None:
           data['categories'] = [
               {
                   "id": self.category_WooId
               }
           ]

        if self.status != None:
           data['status'] = self.status

        if self.image_WooId != None:
            if self.no_image == False:
                data['images'] = [
                    {
                        "id": self.image_WooId,
                        "name": self.name,
                        "alt": self.name
                    },
                ]
            else:
                data['images'] = [
                    {
                        "id": self.image_WooId
                    },
                ]

        if self.button_text != None and self.button_text != '':
           data['button_text'] = self.button_text,
        if self.purchase_note != None and self.purchase_note != '':
           data['purchase_note'] = self.purchase_note,
        if self.weight != None and self.weight != '':
           data['weight'] = self.weight,
        if self.dimension_height != None and self.dimension_height != '':
           data['dimension'] = [
               {
                   "height": str(self.dimension_height),
                   "length": str(self.dimension_length),
                   "width": str(self.dimension_width)
               },
           ]

        if len(self.attributes)>0:
            data['attributes'] = []
            for attr in self.attributes:
                a = {
                    "id": attr['id'],
                    "name": attr['name'],
                    "position": 0,
                    "options": [attr['value'],],
                    }
                data['attributes'].append(a)

        self.data_wooApi = data

    def _buildDataDb(self):
        data = {
            'sku': self.sku,
        }
        if self.woocommerce_id != None:
           data['woocommerce_id'] = self.woocommerce_id
        if self.name != None:
           data['name'] = self.name
        if self.description != None:
           data['description'] = self.description
        if self.short_description != None:
           data['short_description'] = self.short_description
        if self.slug != None:
           data['slug'] = self.slug
        if self.regular_price != None:
           data['regular_price'] = float(self.regular_price)
        if self.category != None:
           data['category'] = self.category
        if self.category_DbId != None:
           data['category_DbId'] = self.category_DbId
        if self.category_WooId != None:
           data['category_WooId'] = self.category_WooId
        if self.status != None:
           data['status'] = self.status
        if self.image_WooId != None:
           data['image_WooId'] = self.image_WooId
        if self.image_DbId != None:
           data['image_DbId'] = self.image_DbId
        data['image_name'] = self.image_name
        data['no_image'] = self.no_image
        if self.button_text != None:
           data['button_text'] = self.button_text
        if self.purchase_note != None:
           data['purchase_note'] = self.purchase_note
        if self.weight != None:
           data['weight'] = self.weight
        if self.dimension_height != None:
           data['dimension_height'] = self.dimension_height
        if self.dimension_length != None:
           data['dimension_length'] = self.dimension_length
        if self.dimension_width != None:
           data['dimension_width'] = self.dimension_width

        if len(self.attributes)>0:
            for attr in self.attributes:
                if attr['name'] in self.model_cls._meta.columns:
                    data[attr['name']] = attr['value']

        self.data_db = data


    def _findImageByWooID(self):
        # Interrogo semplicemente il Database che mi restituisce le informazioni che mi servono
        try:
            image = m.WpMedia.filter(woocommerce_id=self.image_WooId).get()
            if image is not None:
                self.image_name = image.slug
                self.image_DbId = image.id
        except m.WpMedia.DoesNotExist:
                image = m.WpMedia.filter(slug='no_foto').get()
                self.image_name = 'None'
                self.image_DbId = image.id
                self.no_image = True
    
    def _findImageByName(self):
       # in questo caso costruisco un DTO e vedo se esiste (in futuro posso chiedere al DTO di costruire il record)
       image = WpMediaDTO(self.image_name, **{})
       if image.exist():
          self.image_WooId = image.woocommerce_id
          self.image_DbId = image.db_id
       else:
          image = WpMediaDTO('no_foto', **{})
          self.image_WooId = image.woocommerce_id
          self.image_DbId = image.db_id
          self.no_image = True

    def _findCategoryByWooID(self):
        cat = WpCategoryDTO.findCategoryByWooID(self.category_WooId)
        if cat is not None:
            self.category = cat.name
            self.category_DbId = cat.id
            self.category_WooId = cat.woocommerce_id
        else:
            pass

    def _findCategoryByName(self):
        cat = WpCategoryDTO.findCategoryByName(self.category, self.prevCategory)
        if cat:
            self.category_DbId = cat.db_id
            self.category_WooId = cat.woocommerce_id

    def _findAttributesByWooID(self, attr):
        # Interrogo semplicemente il Database che mi restituisce le informazioni che mi servono
        try:
            res = m.WpAttribute.filter(woocommerce_id=attr['id']).get()
            if res is not None:
                dict_attr = {
                    'id': attr['id'],
                    'name': res.slug,
                    'value': attr['options'][0]
                }
                self.attributes.append(dict_attr)
        except m.WpAttribute.DoesNotExist:
            exit(-1)

    def _findAttributeByName(self, slug_attr, value_attr):
        # in questo caso costruisco un DTO e vedo se esiste altrimenti lo creo
        attribute_DbId = None
        attribute_WooId = None
        attributeValue_WooId = None
        attributeValue_DbId = None
        res = WpAttributeDTO(slug_attr)
        if res.exist():
            attribute_DbId = res.db_id
            attribute_WooId = res.woocommerce_id
        else:
            # Creo l'attributo!!
            res.dto2WooApi()
            attribute_DbId = res.db_id
            attribute_WooId = res.woocommerce_id

        # controllo anche che esista il valore dell'attributo
        if attribute_DbId is not None and attribute_WooId is not None:
            res = WpAttributeValueDTO(value_attr, attribute_WooId, attribute_DbId)
            if res.exist():
                attributeValue_DbId = res.db_id
                attributeValue_WooId = res.woocommerce_id
            else:
                # Creo l'attributo!!
                res.dto2WooApi()
                attributeValue_DbId = res.db_id
                attributeValue_WooId = res.woocommerce_id

        if attribute_DbId is not None and attribute_WooId is not None and attributeValue_DbId is not None and attributeValue_WooId is not None:
            dict_attr = {
                'id': attribute_WooId,
                'name': slug_attr,
                'value': value_attr
            }
            self.attributes.append(dict_attr)
        
        
