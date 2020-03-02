from django import template
from quickswap.models import Category

register = template.Library()

@register.inclusion_tag('quickswap/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'current_category': current_category}
