from formskit.validators import NotEmpty as NotEmptyOriginal


class NotEmpty(NotEmptyOriginal):
    message = 'Te pole nie może być puste!'
