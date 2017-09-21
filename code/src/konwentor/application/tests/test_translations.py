from ..translations import KonwentorMessage


class TestKonwentorMessage(object):

    def test_translate(self):
        message = KonwentorMessage()
        message.init('PasswordMustMatch')
        assert message.translate() == 'Email i/lub hasło są błedne.'
