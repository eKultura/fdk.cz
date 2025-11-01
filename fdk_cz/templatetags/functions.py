# templatetags/functions.py

from django import template
import re

register = template.Library()

@register.filter
def replace_url_with_link(value):
    # Regulární výraz pro URL https://fdk.cz
    url_pattern = r"https://fdk\.cz"
    # Nahrazení všech výskytů URL odkazem
    return re.sub(url_pattern, r'<a href="https://fdk.cz">fdk.cz</a>', value)
