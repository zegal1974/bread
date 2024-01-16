from django.urls import path, include

from pages import views

# from pages.views import ActorList

urlpatterns = [
    # path("actors/", ActorList.as_view()),
    # path("api/actor/", )
    path("movie/<str:movie_code>", views.movie),
]
