from haplugin.sql.driver import SqlDriver


class KonwentorDriver(SqlDriver):

    def get_objects(self, **kwargs):
        return self.query(self.model).filter_by(**kwargs)
