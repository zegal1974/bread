from django.urls import path, include
from pages.views import ActorList

urlpatterns = [
    path("actors/", ActorList.as_view()),
    # path("api/actor/", )
    path("movie/<int:movie_code>", ),
]
