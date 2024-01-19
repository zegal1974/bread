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
    acts = Actor.objects.all().order_by('-rating')
    paginator = Paginator(acts, 30)

    page = request.GET.get('page')
    if page and page.isdigit():
        start_page = int(page)
    else:
        start_page = 1

    page_actors = paginator.get_page(start_page)
    context = {'page_actors': page_actors}
    return render(request, 'actors.html', context)


def actor(request, actor_id):
    a = get_object_or_404(Actor, id=actor_id)
    breadcrumbs = [
        {'url': reverse('home'), 'title': '首页'},
        {'url': reverse('actors'), 'title': '演员'},
        {'url': '', 'title': a.name},  # 当前页面不提供URL，仅显示标题
    ]
    context = {'actor': a, 'breadcrumbs': breadcrumbs}
    return render(request, 'actor.html', context)


def movies(request):
    ms = Movie.objects.all()
    pagination = Paginator(ms, 30)
    page = request.GET.get('page')
    if page and page.isdigit() and int(page) > 0:
        start_page = int(page)
    else:
        start_page = 1

    page_movies = pagination.get_page(start_page)
    context = {'page_movies': page_movies}
    print(page_movies.number, page_movies.has_previous(), page_movies.has_next(), page_movies.paginator.page_range)
    return render(request, 'movies.html', context)


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
