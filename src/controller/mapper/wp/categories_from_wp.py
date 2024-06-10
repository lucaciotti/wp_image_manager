from ...dto.wp.category import WpCategoryDTO
from src.provider.wooApi import wooApi

class CategoriesFromWp:

    cat_list = []

    def _retriveAllCategories(self):
        _wooApi = wooApi()
        page = 1
        while True:
            cats = _wooApi.getWooInstance('products/categories', {'per_page': 100, 'page': page})
            if len(cats) == 0:  # no more products
                break
            page = page + 1
            self.cat_list = self.cat_list + cats
    
    def _saveListToDb(self):
        for cat in self.cat_list:
            name = cat['name']
            parent = cat['parent']
            catDTO = WpCategoryDTO(name, parent, **cat)
            catDTO.dto2DB()

    def sync(self):
        self._retriveAllCategories()
        self._saveListToDb()
