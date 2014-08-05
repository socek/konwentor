from formskit.validators import NotEmpty as NotEmptyOriginal
from formskit.validators import IsDigit as IsDigitOriginal


class NotEmpty(NotEmptyOriginal):
    message = 'Te pole nie może być puste.'


class IsDigit(IsDigitOriginal):
    message = 'Ten element musi być liczbą.'
