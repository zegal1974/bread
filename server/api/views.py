from .models.models import Actor
from .serializers import ActorSerializer
from rest_framework import generics


class ActorList(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ActorRetrieve(generics.RetrieveAPIView):
    # queryset = Actor.objects.get()
    pass
