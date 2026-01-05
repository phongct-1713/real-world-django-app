from rest_framework import serializers
from .models import Article, Comment, Tag
from profiles.serializers import ProfileSerializer

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """
    class Meta:
        model = Tag
        fields = ['tag']

class TagRelatedField(serializers.RelatedField):
    """
    Custom field to handle tag relationships.
    """
    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):
        tag, created = Tag.objects.get_or_create(tag=data)
        return tag

    def to_representation(self, value):
        return value.tag

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article model.
    """
    slug = serializers.SlugField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    tagList = TagRelatedField(many=True, required=False, source='tags')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'body', 'tagList',
            'createdAt', 'updatedAt', 'favorited', 'favoritesCount', 'author'
        ]

    def get_favorited(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        if not request.user.is_authenticated:
            return False
        return obj.favorited_by.filter(pk=request.user.pk).exists()

    def get_favoritesCount(self, obj):
        return obj.favorited_by.count()

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        author = self.context['request'].user
        article = Article.objects.create(author=author, **validated_data)
        
        for tag in tags:
            article.tags.add(tag)
        
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update slug if title changed
        if 'title' in validated_data:
            instance.slug = instance._generate_unique_slug()
        
        instance.save()
        
        if tags is not None:
            instance.tags.clear()
            for tag in tags:
                instance.tags.add(tag)
        
        return instance

class ArticleListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing articles (without body for performance).
    """
    slug = serializers.SlugField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    tagList = TagRelatedField(many=True, read_only=True, source='tags')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'tagList',
            'createdAt', 'updatedAt', 'favorited', 'favoritesCount', 'author'
        ]

    def get_favorited(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        if not request.user.is_authenticated:
            return False
        return obj.favorited_by.filter(pk=request.user.pk).exists()

    def get_favoritesCount(self, obj):
        return obj.favorited_by.count()

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """
    id = serializers.IntegerField(read_only=True)
    body = serializers.CharField(required=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'createdAt', 'updatedAt', 'author']

    def create(self, validated_data):
        article = self.context['article']
        author = self.context['request'].user
        return Comment.objects.create(
            author=author,
            article=article,
            **validated_data
        )
