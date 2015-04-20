from pytest import raises

from haplugin.sql.testing import DriverFixture

from ..driver import RoomDriver, get_one_of


class TestDriverRoom(DriverFixture):

    def _get_driver_class(self):
        return RoomDriver

    def test_create(self, fdriver, fixtures, db):
        obj = fdriver.create(
            'myname', convent_id=fixtures['Convent']['first'].id)
        db.flush()
        try:
            assert obj.name == 'myname'
            assert obj.convent == fixtures['Convent']['first']
        finally:
            db.delete(obj)
            db.flush()


class TestGetOneOf(object):

    def test_when_no_value(self):
        """
        get_one_of should raise attribute error when no value was specyfied
        """
        with raises(AttributeError):
            get_one_of(['convent_id', 'convent'], {})

    def test_when_too_many_values(self):
        """
        get_one_of should raise attribute error when more then one value was
        specyfied
        """
        with raises(AttributeError):
            get_one_of(
                ['convent_id', 'convent'],
                {'convent_id': '1', 'convent': 'convent'}
            )

    def test_when_one_value(self):
        """
        get_one_of should return one value which was specyfied
        """
        assert get_one_of(
            ['convent_id', 'convent'],
            {'convent_id': '2'}
        ) == '2'
