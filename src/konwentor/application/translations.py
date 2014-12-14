from formskit.messages import Message


class KonwentorMessage(Message):
    _translations = {
        'PasswordMustMatch': 'Email i/lub hasło są błedne.',
        'EmailMustExists': 'Email i/lub hasło są błedne.',
        'NotEmpty': 'Te pole nie może być puste.',
        'IsDigit': 'Ten element musi być liczbą.',
        'CSRF token do not match!': 'Token CSRF się nie zgadza.',
        'InList': 'Nie można znaleźć podanego elementu.',
        'GameNameInList': 'Nie znaleziono wybranej gry "{value.value}".',
    }

    def translate(self):
        return self._translations[self.text]
