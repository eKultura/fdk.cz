# templatetags/functions.py

from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplies the value by the argument.
    Usage: {{ value|multiply:2 }}
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def dict_lookup(dictionary, key):
    """
    Looks up a key in a dictionary.
    Usage: {{ my_dict|dict_lookup:"key_name" }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, [])
    return []

@register.filter
def replace_url_with_link(value):
    # Regulární výraz pro URL https://fdk.cz
    url_pattern = r"https://fdk\.cz"
    # Nahrazení všech výskytů URL odkazem
    return re.sub(url_pattern, r'<a href="https://fdk.cz">fdk.cz</a>', value)

@register.filter(name='markdown')
def markdown_format(text):
    """
    Simple Markdown filter supporting basic formatting:
    - **bold** or __bold__
    - *italic* or _italic_
    - `code`
    - [link text](url)
    - # Heading 1
    - ## Heading 2
    - ### Heading 3
    - - List item (unordered)
    - 1. List item (ordered)
    """
    if not text:
        return ''

    # Import html module for unescape
    from html import unescape

    # Unescape any existing HTML entities first (to prevent double-escaping)
    text = unescape(str(text))

    # Escape HTML to prevent XSS
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Headings (must come before bold/italic)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Bold (**text** or __text__)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

    # Italic (*text* or _text_)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)

    # Code (`code`)
    text = re.sub(r'`(.+?)`', r'<code style="background: #f1f5f9; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 0.9em;">\1</code>', text)

    # Links [text](url)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color: #3b82f6; text-decoration: none;">\1</a>', text)

    # Unordered lists
    text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>)', r'<ul style="margin-left: 1.5rem; list-style: disc;">\1</ul>', text, flags=re.DOTALL)

    # Ordered lists
    text = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)

    # Line breaks
    text = text.replace('\n', '<br>')

    return mark_safe(text)

@register.filter
def filter_by_score(queryset, min_score):
    """
    Filters queryset by risk_score >= min_score.
    Usage: {{ risks|filter_by_score:20 }}
    """
    try:
        min_score = int(min_score)
        return [risk for risk in queryset if hasattr(risk, 'risk_score') and risk.risk_score >= min_score]
    except (ValueError, TypeError, AttributeError):
        return queryset

@register.filter
def filter_by_score_range(queryset, score_range):
    """
    Filters queryset by risk_score within a range.
    Usage: {{ risks|filter_by_score_range:"13:19" }}
    """
    try:
        # Split the range string "13:19" into min and max
        if isinstance(score_range, str) and ':' in score_range:
            min_score, max_score = map(int, score_range.split(':'))
        else:
            return queryset

        return [risk for risk in queryset if hasattr(risk, 'risk_score') and min_score <= risk.risk_score <= max_score]
    except (ValueError, TypeError, AttributeError):
        return queryset
