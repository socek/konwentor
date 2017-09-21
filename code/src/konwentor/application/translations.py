from formskit.translation import Translation
from haplugin.formskit.models import PostForm


class KonwentorMessage(Translation):
    _translations = {
        'PasswordMustMatch': 'Email i/lub hasło są błedne.',
        'EmailMustExists': 'Email i/lub hasło są błedne.',
        'NotEmpty': 'Te pole nie może być puste.',
        'IsDigit': 'Ten element musi być liczbą.',
        'CSRF token do not match!': 'Token CSRF się nie zgadza.',
        'InList': 'Nie można znaleźć podanego elementu.',
        'GameNameInList': 'Nie znaleziono wybranej gry "{value.value}".',
        'IsValueInAvalibleValues': 'Nie znaleziono podanej gry.',
        'IsUniqe': 'Wartość tego pola już istnieje w bazie.',
        'input must be the same!': 'Hasła muszą się zgadzać!',
    }

    def translate(self):
        return self._translations[self.text]


class KonwentorForm(PostForm):
    translation_class = KonwentorMessage
