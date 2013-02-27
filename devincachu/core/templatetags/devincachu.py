import markdown as m

from django import template
from django.utils import safestring

register = template.Library()


@register.filter(name="markdown")
def markdown(value):
    return safestring.mark_safe(m.markdown(value))
