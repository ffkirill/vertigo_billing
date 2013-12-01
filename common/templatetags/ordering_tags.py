from __future__ import unicode_literals
from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def ordering(context, text, order_by):
    current_direction = context.get('ordering')
    current_order_by = context.get('order_by')
    if not current_order_by:
        return text
    direction = "asc"
    direction_symbol = ""
    active = (current_order_by == order_by)
    if active:
        if not current_direction or current_direction == "asc":
            direction="desc"
        direction_symbol = "&darr; " if direction == "desc" else "&uarr; "
    return '<a href="?order_by={0}&ordering={1}">{3}{2}</a>'.format(
        order_by,
        direction,
        text,
        direction_symbol
    )
