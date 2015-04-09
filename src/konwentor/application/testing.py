from hatak.testing import ControllerFixture as BaseControllerFixture
from haplugin.sql.testing import DatabaseFixture
from haplugin.formskit.testing import FormControllerFixture
from haplugin.formskit.testing import FormFixture as BaseFormFixture


class ControllerFixture(
    BaseControllerFixture,
    DatabaseFixture,
    FormControllerFixture,
):
    pass


class FormFixture(
    BaseFormFixture,
    DatabaseFixture,
):
    pass
