from django.shortcuts import render, get_object_or_404

import logging

from core.models import Movie, Actor

# Create your views here.
# class ActorList(request, startPage=1, perPage=30):
#     actors = Actor.objects.all()

logger = logging.getLogger('pages.view')


def movie(request, movie_code):
    # m1 = Movie.objects.get(code=movie_code)
    #
    # logger.error(f"{movie_code}:  {m1}")

    m = get_object_or_404(Movie, code=movie_code)
    return render(request, 'movie.html', {'movie': m})
