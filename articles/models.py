from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

class Tag(models.Model):
    """
    Tag model for categorizing articles.
    """
    tag = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.tag

class Article(models.Model):
    """
    Article model.
    """
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorites',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        """Generate a unique slug for the article."""
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{uuid.uuid4().hex[:6]}'
            num += 1
        return unique_slug

    @property
    def favorites_count(self):
        return self.favorited_by.count()

class Comment(models.Model):
    """
    Comment model for articles.
    """
    body = models.TextField()
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'
