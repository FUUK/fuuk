from django.forms import CharField


class NullCharField(CharField):
    def to_python(self, value):
        "Returns Unicode or None. postpone to save?"
        value = super(CharField, self).to_python(value)
        if value == '':
            return None
        return value
