from django.shortcuts import render, get_object_or_404

from core.models import Movie, Actor


# Create your views here.
# class ActorList(request, startPage=1, perPage=30):
#     actors = Actor.objects.all()


def movie(request, movie_code):
    m = get_object_or_404(Movie, code=movie_code)
    return render(request, 'templates/movie.html', {'movie': m})
