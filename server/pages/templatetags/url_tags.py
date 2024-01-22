from django import template

register = template.Library()


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


@register.simple_tag(takes_context=True)
def active_menu(context, menu_items):
    request = context['request']
    current_path = request.path_info

    for item in menu_items:
        # current_path.startswith(item['url'])
        if current_path == item['url']:
            item['active'] = True
        else:
            item['active'] = False

    return menu_items
