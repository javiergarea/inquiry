import re
from django import template

register = template.Library()

@register.filter(name='remove_page')
def remove_page(url):
    url = re.sub('&page=[0-9]+', '', url)
    return url