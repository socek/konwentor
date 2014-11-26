from haplugin.toster import TestCase
from ..translations import KonwentorMessage


class KonwentorMessageTests(TestCase):
    prefix_from = KonwentorMessage

    def test_translate(self):
        message = self.prefix_from()
        message.init('PasswordMustMatch')
        self.assertEqual(
            'Email i/lub hasło są błedne.',
            message.translate())
