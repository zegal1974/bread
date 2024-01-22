from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

import logging

from django.urls import reverse, reverse_lazy

from core.models import Movie, Actor, Video

logger = logging.getLogger('pages.view')

MENU_ITEMS = [
    {'url': reverse_lazy('home'), 'title': 'Home', 'icon': 'home'},
    {'url': reverse_lazy('actors'), 'title': 'Actors', 'icon': 'user'},
    {'url': reverse_lazy('movies'), 'title': 'Movies', 'icon': 'clapperboard'},
    {'url': reverse_lazy('settings'), 'title': 'Settings', 'icon': 'gear'},
]


def home(request):
    breadcrumbs = [
        {'url': '', 'title': 'Home'},
    ]

    statistics = {
        'count_actors': Actor.objects.count(),
        'count_movies': Movie.objects.count(),
        'count_videos': Video.objects.count(),
    }

    context = {'statistics': statistics, 'breadcrumbs': breadcrumbs, 'menu_items': MENU_ITEMS}
    return render(request, 'home.html', context)


def actors(request):
    breadcrumbs = [
        {'url': reverse('home'), 'title': 'Home'},
        {'url': '', 'title': 'Actor'},
    ]

    acts = Actor.objects.all().order_by('-rating')
    paginator = Paginator(acts, 30)

    page = request.GET.get('page')
    if page and page.isdigit():
        start_page = int(page)
    else:
        start_page = 1

    page_actors = paginator.get_page(start_page)
    context = {'page_actors': page_actors, 'breadcrumbs': breadcrumbs, 'menu_items': MENU_ITEMS}
    return render(request, 'actors.html', context)


def actor(request, actor_id):
    a = get_object_or_404(Actor, id=actor_id)
    breadcrumbs = [
        {'url': reverse('home'), 'title': 'Home'},
        {'url': reverse('actors'), 'title': 'Actor'},
        {'url': '', 'title': a.name},  # 当前页面不提供URL，仅显示标题
    ]
    context = {'actor': a, 'breadcrumbs': breadcrumbs, 'menu_items': MENU_ITEMS}
    return render(request, 'actor.html', context)


def movies(request):
    breadcrumbs = [
        {'url': reverse('home'), 'title': 'Home'},
        {'url': '', 'title': 'Movies'},
    ]

    ms = Movie.objects.all()
    pagination = Paginator(ms, 30)
    page = request.GET.get('page')
    if page and page.isdigit() and int(page) > 0:
        start_page = int(page)
    else:
        start_page = 1

    page_movies = pagination.get_page(start_page)
    context = {'page_movies': page_movies, 'breadcrumbs': breadcrumbs, 'menu_items': MENU_ITEMS}
    return render(request, 'movies.html', context)


def movie(request, movie_code):
    m = get_object_or_404(Movie, code=movie_code)
    breadcrumbs = [
        {'url': reverse('home'), 'title': 'Home'},
        {'url': reverse('movies'), 'title': 'Movies'},
        {'url': '', 'title': m.code},  # 当前页面不提供URL，仅显示标题
    ]
    context = {'movie': m, 'breadcrumbs': breadcrumbs, 'menu_items': MENU_ITEMS}
    return render(request, 'movie.html', context)


def settings(request):
    breadcrumbs = [
        {'url': reverse('home'), 'title': 'Home'},
        {'url': '', 'title': 'Settings'},
    ]

    context = {'breadcrumbs': breadcrumbs, 'menu_items': MENU_ITEMS}
    return render(request, 'settings.html', context)
