import json

from ...dto.wp.product import WpProductDTO
from src.provider.wooApi import wooApi
from src.provider.storage import RepoStorage

class ProductsFromXls:
    mapped_columns = None
    map_columns_by_num = None
    map_columns_by_name = None

    def __init__(self):
        self.repoStorage = RepoStorage()
        self.path = self.repoStorage.getBasePath()
        self.file_by_num = self.repoStorage.getFile(self.path, "map_columns.json")
        self.file_by_name = self.repoStorage.getFile(self.path, "map_columns_by_name.json")

        with open(self.file_by_num, mode="r", encoding="utf-8") as json_file:
            self.map_columns_by_num = json.load(json_file)
        
        self.map_columns_by_num = {k: int(v) for k, v in self.map_columns_by_num.items() if v}

        with open(self.file_by_name, mode="r", encoding="utf-8") as json_file:
            self.map_columns_by_name = json.load(json_file)

        self.map_columns_by_name = {str(v): str(k) for k, v in self.map_columns_by_name.items() if v}

    def dinamicMapColumnsByHeader(self, headerRow):
        dColumns={}
        for pos, cell in enumerate(headerRow):
            if cell.value.lower() in self.map_columns_by_name:
                dColumns[self.map_columns_by_name[cell.value.lower()]] = pos
        
        if 'sku' not in dColumns:
            return None

        self.mapped_columns = dColumns

    def mapToDto(self, row):
        if self.mapped_columns is None:
            self.mapped_columns = self.map_columns_by_num

        data = {}
        sku = None
        for k, v in self.mapped_columns.items():
            if k!='sku':
                data[k] = row[v].value.replace(r'\r\n', r'\n').replace('_x000D_', '').replace(r"\n", '<br>') if isinstance(row[v].value, str) else row[v].value
            else:
                sku = row[v].value

        if sku is not None:
            return WpProductDTO(sku, **data)
        else:
            return None
        