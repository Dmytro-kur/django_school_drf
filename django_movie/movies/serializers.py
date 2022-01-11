from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class MovieListSerializer(serializers.ModelSerializer):
    """Movie List"""
    rating_user = serializers.BooleanField()
    # middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = (
            "id", "title", "tagline", "category", 
            "rating_user", #"middle_star", "poster"
        )


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Add review"""

    class Meta:
        model = Review
        fields = "__all__"


class RecursiveSerializer(serializers.Serializer):
    """Display children recursively"""
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    """Review filter for parents only"""
    def to_representation(self, data):
        print("DATA: ", data.all())
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewSerializer(serializers.ModelSerializer):
    """Display review"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Movie description"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )
    # directors = ActorListSerializer(read_only=True, many=True)
    actors = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )
    # actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Ading rating by users"""
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star':validated_data.get('star')}
        )
        return rating

# class ReviewSerializer(serializers.ModelSerializer):
#     """Display Reviews"""
#     children = RecursiveSerializer(many=True)

#     class Meta:
#         list_serializer_class = FilterReviewListSerializer
#         model = Review
#         fields = ("id", "name", "text", "children")


# class FilterReviewListSerializer(serializers.ListSerializer):
#     """Фильтр комментариев, только parents"""
#     def to_representation(self, data):
#         data = data.filter(parent=None)
#         return super().to_representation(data)


# class RecursiveSerializer(serializers.Serializer):
#     """Вывод рекурсивно children"""
#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         return serializer.data


# class ActorListSerializer(serializers.ModelSerializer):
#     """Вывод списка актеров и режиссеров"""
#     class Meta:
#         model = Actor
#         fields = ("id", "name", "image")


# class ActorDetailSerializer(serializers.ModelSerializer):
#     """Вывод полного описани актера или режиссера"""
#     class Meta:
#         model = Actor
#         fields = "__all__"


# class CreateRatingSerializer(serializers.ModelSerializer):
#     """Добавление рейтинга пользователем"""
#     class Meta:
#         model = Rating
#         fields = ("star", "movie")

#     def create(self, validated_data):
#         rating, _ = Rating.objects.update_or_create(
#             ip=validated_data.get('ip', None),
#             movie=validated_data.get('movie', None),
#             defaults={'star': validated_data.get("star")}
#         )
#         return rating
