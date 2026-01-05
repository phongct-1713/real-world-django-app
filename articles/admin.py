from django.contrib import admin
from .models import Article, Comment, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    search_fields = ('tag',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'description', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('body',)
    ordering = ('-created_at',)
