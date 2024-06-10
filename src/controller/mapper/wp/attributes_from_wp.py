from ...dto.wp.attribute import WpAttributeDTO, WpAttributeValueDTO
from src.provider.wooApi import wooApi

class AttributesFromWp:

    atr_list = []
    atr_values_list = []

    def _retriveAllAttributes(self):
        _wooApi = wooApi()
        res = _wooApi.getWooInstance('products/attributes')
        self.atr_list = self.atr_list + res

    def _retriveAllAttributesValues(self, attrId):
        _wooApi = wooApi()
        page = 1
        while True:
            res = _wooApi.getWooInstance('products/attributes/{}/terms'.format(attrId), {'per_page': 100, 'page': page})
            if len(res) == 0:  # no more products
                break
            page = page + 1
            self.atr_values_list = self.atr_values_list + res

    def _saveListToDb(self):
        for atr in self.atr_list:
            slug = atr['slug']
            atrDTO = WpAttributeDTO(slug, **atr)
            atrDTO.dto2DB()
            self.atr_values_list = []
            self._retriveAllAttributesValues(atrDTO.woocommerce_id)
            for atr_val in self.atr_values_list:
                slug = atr_val['slug']
                atrValDTO = WpAttributeValueDTO(slug, atrDTO.woocommerce_id, atrDTO.db_id, **atr_val)
                atrValDTO.dto2DB()

    def sync(self):
        self._retriveAllAttributes()
        self._saveListToDb()
