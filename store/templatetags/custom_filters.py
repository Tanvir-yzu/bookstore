from django import template

register = template.Library()

# Register your custom filters here
# Example:
@register.filter(name='example_filter')
def example_filter(value):
    return value