from src.provider.logger import Logger
from src.provider.typerHandler import TyperCmdHandler
from src.provider.wooApi import wooApi
from src.models import wp as m
from ...dto.wp.product import WpProductDTO
from ...dto.wp.category import WpCategoryDTO
import typer

class ProductsBatchToWp:
    data = {
        'update': [],
        'create': []
    }
    counter = 0
    logger = Logger()

    def addProduct(self, product):
        if product.data_wooApi == None:
            message = '--> Error Data Json: "%s"' % (product.sku)
            typer.secho(message=message, fg=typer.colors.RED)
        else:
            if (product.woocommerce_id != None):
                # update
                self.data['update'].append(product.data_wooApi)
                self.logger.debug(f'Update Batch Product: {product.sku}: {product.data_wooApi}')
            else:
                # create
                self.data['create'].append(product.data_wooApi)
                self.logger.debug(f'Create Batch Product: {product.sku}: {product.data_wooApi}')
            self.counter += 1

        if self.counter == 100:
            self.execute()
            self.counter = 0
            self.data = {
                'update': [],
                'create': []
            }

    def execute(self):
        if self.counter > 0:
            _wooApi = wooApi()
            # print(self.data)
            res = _wooApi.batchWooInstance('products/batch', self.data)
            if res == 1:
                self.logger.debug(f'Batch Execution')
            else:
                self.logger.criticalExpLog(f'Batch execution')


class SetProductPrivateByCategory:
    verbose = False
    category_name = ''
    category_id = None
    products_list = []
    data = {
        'update': [],
        'create': []
    }
    counter = 0
    logger = Logger()
    typerHandler = TyperCmdHandler()

    def __init__(self, category_name, verbose=False):
        self.category_name = category_name
        self.verbose = verbose

    def _retriveAllCategoryProducts(self):
        prod_list = m.WpProduct.select().where(m.WpProduct.category_WooId == self.category_id, m.WpProduct.status == 'publish')
        if prod_list is not None:
            self.products_list = prod_list

    def _setPrivateAllProducts(self):
        for prod in self.products_list:
            sku = prod.sku
            data_json = {
                'id': prod.woocommerce_id,
                'status': 'private'
            }
            self.data['update'].append(data_json)
            self.logger.debug(f'SET_PRIVATE Product {sku}: {data_json}')
            self.counter += 1
            if self.counter == 100:
                self._updateProducts()
                self.counter = 0
                self.data = {
                    'update': [],
                    'create': []
                }
        self._updateProducts()
        self.counter = 0
        self.data = {
            'update': [],
            'create': []
        }

    def _updateProducts(self):
        if self.counter > 0:
            _wooApi = wooApi()
            # print(self.data)
            res = _wooApi.batchWooInstance('products/batch', self.data)
            if res == 1:
                self.logger.debug(f'Batch Execution')
            else:
                self.logger.criticalExpLog(f'Batch execution')

    def execute(self):
        cat = WpCategoryDTO.findCategoryByName(self.category_name, create=False)
        if cat:
            self.category_id = cat.woocommerce_id
        if self.category_id is not None:
            self._retriveAllCategoryProducts()
            if len(self.products_list) > 0:
                self._setPrivateAllProducts()
                self.typerHandler.echoGreen('ProductSetPrivateByCategory: CATEGORY "%s" -> UPDATE ENDED!')
            else:
                self.typerHandler.echoRed('ProductSetPrivateByCategory: CATEGORY "%s" -> PRODUCTS NOT FOUND!')
        else:
            self.typerHandler.echoRed('ProductSetPrivateByCategory: CATEGORY "%s" NOT FOUND!')
