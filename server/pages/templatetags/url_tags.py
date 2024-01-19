from django import template
from django.template.loader import select_template

from core.models import Producer, Actor

register = template.Library()


# @register.simple_tag()
# def render_producer(context, producer: Producer):
#     if not producer:
#         return ""
#
#     return ""

@register.filter
def url_avatar(actor_link):
    if actor_link:
        return actor_link
    else:
        return "https://dummyimage.com/125x125/caf4fa/"


@register.filter
def url_movie_thumb(thumb_link):
    if thumb_link:
        return thumb_link
    else:
        return "https://dummyimage.com/147x200/caf4fa/"
