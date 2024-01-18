from django.urls import path, include

from pages import views

# from pages.views import ActorList

urlpatterns = [
    # path("actors/", ActorList.as_view()),
    # path("api/actor/", )
    path("", views.home, name='home'),
    path("actors", views.actors, name='actors'),
    path("actors/<str:actor_id>/", views.actor, name='actor'),
    path("movies", views.movies, name='movies'),
    path("movies/<str:movie_code>", views.movie, name='movie'),
]
