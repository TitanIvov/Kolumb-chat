# core/serializers.py
from rest_framework import serializers
from .models import CustomUser, Route, Point, Tag, Category
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'nickname', 'email', 'phone', 'gender',
            'bio', 'country', 'city', 'language', 'birth_date',
            'date_joined', 'last_login', 'followers', 'friends'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PointSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Point
        fields = [
            'id', 'latitude', 'longitude', 'name', 'description',
            'point_type', 'tags', 'country', 'city', 'street', 'house',
            'is_verified', 'working_hours', 'min_price', 'max_price',
            'metadata', 'visits', 'rating', 'status', 'routes', 'created_at',
            'updated_at', 'creator'
        ]
        extra_kwargs = {
            'working_hours': {'write_only': True},
            'metadata': {'write_only': True},
            'routes': {'required': False}
        }


class RouteSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)
    start_point = serializers.PrimaryKeyRelatedField(queryset=Point.objects.all())
    end_point = serializers.PrimaryKeyRelatedField(queryset=Point.objects.all())
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Route
        fields = [
            'id', 'title', 'creator', 'categories', 'tags', 'country',
            'city', 'street', 'created_at', 'updated_at', 'difficulty',
            'min_price', 'max_price', 'rating', 'completions', 'metadata',
            'status', 'duration', 'start_point', 'end_point', 'distance',
            'activity_type'
        ]
        read_only_fields = ['rating', 'completions']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        tags_data = validated_data.pop('tags', [])

        route = Route.objects.create(**validated_data)

        for category in categories_data:
            route.categories.add(category)

        for tag in tags_data:
            route.tags.add(tag)

        return route


class RouteDetailSerializer(RouteSerializer):
    points = PointSerializer(many=True, read_only=True)
    start_point = PointSerializer(read_only=True)
    end_point = PointSerializer(read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta(RouteSerializer.Meta):
        fields = RouteSerializer.Meta.fields + ['points']


class PointDetailSerializer(PointSerializer):
    routes = RouteSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta(PointSerializer.Meta):
        fields = PointSerializer.Meta.fields