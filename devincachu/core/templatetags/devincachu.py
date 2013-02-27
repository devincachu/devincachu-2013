import markdown as m

from django import template

register = template.Library()


@register.filter(name="markdown")
def markdown(value):
    return m.markdown(value)
