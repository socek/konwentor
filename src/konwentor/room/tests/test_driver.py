from haplugin.sql.testing import DriverFixture

from ..driver import RoomDriver


class TestDriverRoom(DriverFixture):

    def _get_driver_class(self):
        return RoomDriver

    def test_create(self, fdriver, fixtures, db):
        obj = fdriver.create('myname', fixtures['Convent']['first'].id)
        db.flush()
        try:
            assert obj.name == 'myname'
            assert obj.convent == fixtures['Convent']['first']
        finally:
            db.delete(obj)
            db.flush()
