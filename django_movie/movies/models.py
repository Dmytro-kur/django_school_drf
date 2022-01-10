from django.db import models
from datetime import date
from django.urls import reverse


class Category(models.Model):
    """Categories"""
    name = models.CharField(max_length=150)
    description = models.TextField()
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    """Actors and producers"""
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Actors and producers"
        verbose_name_plural = "Actors and producers"


class Genre(models.Model):
    """Genre"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    """Movies"""
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100, default='')
    description = models.TextField()
    poster = models.ImageField(upload_to="movies/")
    year = models.PositiveSmallIntegerField(default=2019)
    country = models.CharField(max_length=30)
    directors = models.ManyToManyField(
        Actor, verbose_name="directors", related_name="film_director"
    )
    actors = models.ManyToManyField(
        Actor, verbose_name="actors", related_name="film_actor"
    )
    genres = models.ManyToManyField(Genre, verbose_name="genres")
    world_premiere = models.DateField(default=date.today)
    budget = models.PositiveIntegerField(
        default=0, help_text="type amount in dollars"
    )
    fees_in_usa = models.PositiveIntegerField(
        default=0, help_text="type amount in dollars"
    )
    fess_in_world = models.PositiveIntegerField(
        default=0, help_text="type amount in dollars"
    )
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.SET_NULL, 
        null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class MovieShots(models.Model):
    """Movie Shots"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="movie_shots/")
    movie = models.ForeignKey(
        Movie, verbose_name="Movies", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie Shots"
        verbose_name_plural = "Movie Shots"


class RatingStar(models.Model):
    """Rating Star"""
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField(max_length=15)
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name="star"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="movie",
        related_name="ratings"
    )

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Review(models.Model):
    """Review"""
    email = models.EmailField()
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, 
        null=True, related_name="children"
    )
    movie = models.ForeignKey(
        Movie, verbose_name="movie", on_delete=models.CASCADE, 
        related_name="reviews"
    )

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
