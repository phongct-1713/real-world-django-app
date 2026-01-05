from django.urls import path

from .views import (
    ArticleListCreateAPIView,
    ArticleFeedAPIView,
    ArticleRetrieveUpdateDestroyAPIView,
    ArticleFavoriteAPIView,
    CommentListCreateAPIView,
    CommentDestroyAPIView,
    TagListAPIView,
)

app_name = 'articles'

urlpatterns = [
    path('articles/', ArticleListCreateAPIView.as_view(), name='article-list-create'),
    path('articles/feed/', ArticleFeedAPIView.as_view(), name='article-feed'),
    path('articles/<slug:slug>/', ArticleRetrieveUpdateDestroyAPIView.as_view(), name='article-detail'),
    path('articles/<slug:slug>/favorite/', ArticleFavoriteAPIView.as_view(), name='article-favorite'),
    path('articles/<slug:slug>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('articles/<slug:slug>/comments/<int:pk>/', CommentDestroyAPIView.as_view(), name='comment-delete'),
    path('tags/', TagListAPIView.as_view(), name='tags'),
]
