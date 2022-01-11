from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from rest_framework import generics, permissions, viewsets
from .service import get_client_ip
# from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor, Review
from .serializers import (
    CreateRatingSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    # CreateRatingSerializer,
    # ActorListSerializer,
    # ActorDetailSerializer,
)


class MovieListView(APIView):
    """List of movies"""
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Case(
                models.When(ratings__ip=get_client_ip(request), then=True),
                default=False,
                output_field=models.BooleanField()
            )
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Movie detail"""
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Add review to film"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Adding a movie's rating"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)

