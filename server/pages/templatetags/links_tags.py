from django import template
from django.template.loader import select_template

from core.models import Producer

register = template.Library()

# @register.simple_tag()
# def render_producer(context, producer: Producer):
#     if not producer:
#         return ""
#
#     return ""