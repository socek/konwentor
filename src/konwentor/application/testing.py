from pytest import yield_fixture
from mock import patch

from hatak.testing import ControllerFixture as BaseControllerFixture
from haplugin.sql.testing import DatabaseFixture
from haplugin.formskit.testing import FormControllerFixture
from haplugin.formskit.testing import FormFixture as BaseFormFixture


class ControllerFixture(
    BaseControllerFixture,
    DatabaseFixture,
    FormControllerFixture,
):
    @yield_fixture
    def add_helper(self, controller):
        with patch.object(controller, 'add_helper') as mock:
            yield mock


class FormFixture(
    BaseFormFixture,
    DatabaseFixture,
):
    pass
