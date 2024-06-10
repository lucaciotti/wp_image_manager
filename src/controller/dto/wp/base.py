from src.provider.logger import Logger
from src.provider.wooApi import wooApi
from src.models import wp as m
from ..base import BaseDTO

class WpBaseDTO(BaseDTO):
    woocommerce_id = None
    data_wooApi = None

    woo_instance = None

    logger = Logger()

    def _buildDataWooApi(self):
        pass
    
    def dto2DB(self):
        self._buildDataDb()
        if self.db_id is None:
            self.db_id, _ = self._dbExist()

        if self.db_id is None:
            record, created = self.model_cls.get_or_create(**self.data_db)
            self.db_id = record.id
            self.woocommerce_id = record.woocommerce_id
            self.logger.info(F'Created {self.model_cls.__name__}: {self.data_db}')
        else:
            self.model_cls.update(**self.data_db).where(self.model_cls.id == self.db_id).execute()
            self.logger.info(F'Updated {self.model_cls.__name__}: {self.data_db}')

    def dto2WooApi(self):
        _wooApi = wooApi()
        self._buildDataWooApi()
        self.woo_instance = self.woo_instance.format(**self.data_db)
        res = -1
        if self.data_wooApi is not None and self.woo_instance is not None and self.data_wooApi is not None:
            if (self.woocommerce_id is not None):
                res = _wooApi.updateWooInstance(self.woo_instance, self.woocommerce_id, self.data_wooApi)
                self.logger.info(F'Updated WooCommerce {self.model_cls.__name__}: {self.data_wooApi}')
            else:
                res = _wooApi.createWooInstance(self.woo_instance, self.data_wooApi)
                self.logger.info(F'Created WooCommerce {self.model_cls.__name__}: {self.data_wooApi}')
                self.woocommerce_id = res['id']
                self.dto2DB()
        return res
