from django import template

register = template.Library()

@register.filter
def getDictValue(dict, key):
    return dict.get(key)
