from pytest import raises
from sqlalchemy.orm.exc import NoResultFound

from haplugin.sql.testing import DriverFixture

from ..driver import ConventDriver


class TestDriverConvent(DriverFixture):

    def _get_driver_class(self):
        return ConventDriver

    def test_get_convent_from_session(
        self,
        fdriver,
        fixtures,
        request
    ):
        """
        .get_convent_from_session shoulre return convent which id was set in
        the session
        """
        request.session = {
            'convent_id': fixtures['Convent']['first'].id
        }

        assert (
            fdriver.get_convent_from_session(request)
            == fixtures['Convent']['first']
        )

    def test_get_convent_from_sesson_when_no_id_set(
        self,
        fdriver,
        fixtures,
        request,
    ):
        """
        .get_convent_from_session shoulre raise NoResultFound error when no
        convent_id set in the session
        """
        request.session = {}

        with raises(NoResultFound):
            fdriver.get_convent_from_session(request)
