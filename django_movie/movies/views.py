from django.db import models
from rest_framework import generics
from .service import get_client_ip, MovieFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    CreateRatingSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)


class MovieListView(generics.ListAPIView):
    """List of movies"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count(
                'ratings', 
                filter=models.Q(ratings__ip=get_client_ip(self.request))
            )
        ).annotate(
            middle_star=models.Sum(
                models.F('ratings__star')
            ) / models.Count(models.F('ratings'))
        )
        
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Movie detail"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer
        


class ReviewCreateView(generics.CreateAPIView):
    """Add review to film"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Adding a movie's rating"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorsListView(generics.ListAPIView):
    """Displaying a list of actors"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Displaying a detail of actors"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer