from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

import logging

from django.urls import reverse

from core.models import Movie, Actor

# Create your views here.
# class ActorList(request, startPage=1, perPage=30):
#     actors = Actor.objects.all()

logger = logging.getLogger('pages.view')


def home(request):
    pass


def actors(request):
    acts = Actor.objects.all()

    paginator = Paginator(acts, 30)

    page = request.GET.get('page')
    if page and page.isdigit():
        start_page = int(page) - 1
    else:
        start_page = 0

    actors_page = paginator.get_page(start_page)

    context = {'actors': actors_page}
    return render(request, 'actors.html', context)


def actor(request, actor_id):
    a = get_object_or_404(Actor, id=actor_id)
    breadcrumbs = [
        {'url': reverse('home'), 'title': '首页'},
        {'url': reverse('actors'), 'title': '演员'},
        {'url': '', 'title': a.actor_id},  # 当前页面不提供URL，仅显示标题
    ]
    context = {'actor': a, 'breadcrumbs': breadcrumbs}
    return render(request, 'actor.html', context)


def movie(request, movie_code):
    # m1 = Movie.objects.get(code=movie_code)
    #
    # logger.error(f"{movie_code}:  {m1}")

    m = get_object_or_404(Movie, code=movie_code)
    breadcrumbs = [
        {'url': reverse('home'), 'title': '首页'},
        # {'url': reverse('movies', args=[article.category.slug]), 'title': article.category.name},
        {'url': '', 'title': m.code},  # 当前页面不提供URL，仅显示标题
    ]
    context = {'movie': m, 'breadcrumbs': breadcrumbs}
    return render(request, 'movie.html', context)
