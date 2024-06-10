from ...dto.wp.product import WpProductDTO
from src.provider.wooApi import wooApi

class ProductsFromWp:

    products_list = []

    def _retriveAllProducts(self):
        _wooApi = wooApi()
        page = 1
        while True:
            products = _wooApi.getWooInstance('products', {'per_page': 100, 'page': page})
            # retrieve ids from **products**
            if len(products) == 0:  # no more products
                break
            page = page + 1
            self.products_list = self.products_list + products
    
    def _saveListToDb(self):
        for prod in self.products_list:
            sku = prod['sku']
            prodDTO = WpProductDTO(sku, **prod)
            prodDTO.dto2DB()

    def sync(self):
        self._retriveAllProducts()
        self._saveListToDb()


