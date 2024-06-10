
class BaseDTO:
    db_id = None
    data_db = None

    model_cls = None

    def _dbExist(self):
        pass
    
    def _buildDataDb(self):
        pass

    def exist(self):
        return True if self.db_id is not None else False
    
    def getDbFieldsList(self):
        return [key for key in self.data_db.keys() if key != 'db_id']


    def dto2DB(self):
        self._buildDataDb()
        if self.db_id is None:
            self.db_id, _ = self._dbExist()

        if self.db_id is None:
            record, created = self.model_cls.get_or_create(**self.data_db)
            self.db_id = record.id
        else:
            self.model_cls.update(**self.data_db).where(self.model_cls.id==self.db_id).execute()
            