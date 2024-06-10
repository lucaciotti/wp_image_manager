from src.controller.base import BaseController
from src.controller.mapper.wp.attributes_from_wp import AttributesFromWp
from src.controller.mapper.wp.categories_from_wp import CategoriesFromWp
from src.controller.mapper.wp.medias_from_wp import MediasFromWp
from src.controller.mapper.wp.products_from_wp import ProductsFromWp


class SyncLocalDBController(BaseController):

    def syncAllTables(self):
        self.syncAttributeTable()
        self.syncCategoryTable()
        self.syncMediaTable()
        self.syncProductTable()

    def syncMediaTable(self):
        try:
            self.typerHandler.echoYellow('Sincronizzazione delle Immagini Iniziata')
            MediasFromWp().sync()
            self.typerHandler.echoGreen('Sincronizzazione delle Immagini TERMINATA')
        except Exception as e:
            self.logger.exeptionLog(repr(e))

    def syncCategoryTable(self):
        try:
            self.typerHandler.echoYellow('Sincronizzazione delle Categorie Iniziata')
            CategoriesFromWp().sync()
            self.typerHandler.echoGreen('Sincronizzazione delle Categorie TERMINATA')
        except Exception as e:
            self.logger.exeptionLog(repr(e))

    def syncAttributeTable(self):
        try:
            self.typerHandler.echoYellow('Sincronizzazione degli Attributi Iniziata')
            AttributesFromWp().sync()
            self.typerHandler.echoGreen('Sincronizzazione degli Attributi TERMINATA')
        except Exception as e:
            self.logger.exeptionLog(repr(e))

    def syncProductTable(self):
        try:
            self.typerHandler.echoYellow('Sincronizzazione dei Prodotti Iniziata')
            ProductsFromWp().sync()
            self.typerHandler.echoGreen('Sincronizzazione dei Prodotti TERMINATA')
        except Exception as e:
            self.logger.exeptionLog(repr(e))