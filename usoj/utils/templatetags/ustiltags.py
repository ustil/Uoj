from django.template import Library
from django.template.defaultfilters import stringfilter


register = Library()


@stringfilter
def spacify(value):
    return value.strip().replace(' ', '&nbsp;')


register.filter(spacify)
