from rest_framework import status, generics
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article, Comment, Tag
from .serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    CommentSerializer,
)

class ArticleListCreateAPIView(APIView):
    """
    List articles or create a new article.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        """
        List articles with optional filters.
        """
        tag = request.query_params.get('tag', None)
        author = request.query_params.get('author', None)
        favorited = request.query_params.get('favorited', None)
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))

        queryset = Article.objects.all()

        if tag:
            queryset = queryset.filter(tags__tag=tag)

        if author:
            queryset = queryset.filter(author__username=author)

        if favorited:
            queryset = queryset.filter(favorited_by__username=favorited)

        queryset = queryset.distinct()[offset:offset + limit]
        
        serializer = ArticleListSerializer(
            queryset,
            many=True,
            context={'request': request}
        )

        return Response({
            'articles': serializer.data,
            'articlesCount': Article.objects.count()
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new article.
        """
        article_data = request.data.get('article', {})
        
        serializer = ArticleSerializer(
            data=article_data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'article': serializer.data}, status=status.HTTP_201_CREATED)

class ArticleFeedAPIView(APIView):
    """
    Get articles from followed users.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))

        # Get users that the current user follows
        followed_users = request.user.follows.all()
        
        queryset = Article.objects.filter(
            author__in=followed_users
        ).distinct()[offset:offset + limit]

        serializer = ArticleListSerializer(
            queryset,
            many=True,
            context={'request': request}
        )

        articles_count = Article.objects.filter(author__in=followed_users).count()

        return Response({
            'articles': serializer.data,
            'articlesCount': articles_count
        }, status=status.HTTP_200_OK)

class ArticleRetrieveUpdateDestroyAPIView(APIView):
    """
    Retrieve, update, or delete an article.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

    def get(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleSerializer(article, context={'request': request})
        return Response({'article': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, slug):
        article = self.get_object(slug)

        if article.author != request.user:
            raise PermissionDenied('You do not have permission to edit this article.')

        article_data = request.data.get('article', {})
        
        serializer = ArticleSerializer(
            article,
            data=article_data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'article': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        article = self.get_object(slug)

        if article.author != request.user:
            raise PermissionDenied('You do not have permission to delete this article.')

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ArticleFavoriteAPIView(APIView):
    """
    Favorite and unfavorite articles.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

    def post(self, request, slug):
        """Favorite an article."""
        article = self.get_object(slug)
        user = request.user

        article.favorited_by.add(user)

        serializer = ArticleSerializer(article, context={'request': request})
        return Response({'article': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        """Unfavorite an article."""
        article = self.get_object(slug)
        user = request.user

        article.favorited_by.remove(user)

        serializer = ArticleSerializer(article, context={'request': request})
        return Response({'article': serializer.data}, status=status.HTTP_200_OK)

class CommentListCreateAPIView(APIView):
    """
    List or create comments for an article.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_article(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

    def get(self, request, slug):
        """Get comments for an article."""
        article = self.get_article(slug)
        comments = article.comments.all()  # type: ignore
        
        serializer = CommentSerializer(
            comments,
            many=True,
            context={'request': request}
        )

        return Response({'comments': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, slug):
        """Create a comment on an article."""
        article = self.get_article(slug)
        comment_data = request.data.get('comment', {})

        serializer = CommentSerializer(
            data=comment_data,
            context={'request': request, 'article': article}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'comment': serializer.data}, status=status.HTTP_201_CREATED)


class CommentDestroyAPIView(APIView):
    """
    Delete a comment.
    """
    permission_classes = (IsAuthenticated,)

    def delete(self, request, slug, pk):
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

        try:
            comment = Comment.objects.get(pk=pk, article=article)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID was not found.')

        if comment.author != request.user:
            raise PermissionDenied('You do not have permission to delete this comment.')

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagListAPIView(APIView):
    """
    List all tags.
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        tags = Tag.objects.all()
        tag_list = [tag.tag for tag in tags]
        return Response({'tags': tag_list}, status=status.HTTP_200_OK)
