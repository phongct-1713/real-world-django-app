"""
Management command to generate seed data for the Conduit application.
Usage: python manage.py seed_data
"""

import random
from django.core.management.base import BaseCommand
from users.models import User
from articles.models import Article, Comment, Tag


class Command(BaseCommand):
    help = 'Generate seed data for the Conduit application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of users to create (default: 5)'
        )
        parser.add_argument(
            '--articles',
            type=int,
            default=20,
            help='Number of articles to create (default: 20)'
        )
        parser.add_argument(
            '--comments',
            type=int,
            default=50,
            help='Number of comments to create (default: 50)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Comment.objects.all().delete()
            Article.objects.all().delete()
            Tag.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write('Creating seed data...')
        
        # Create users
        users = self.create_users(options['users'])
        
        # Create tags
        tags = self.create_tags()
        
        # Create articles
        articles = self.create_articles(options['articles'], users, tags)
        
        # Create comments
        self.create_comments(options['comments'], users, articles)
        
        # Create follows
        self.create_follows(users)
        
        # Create favorites
        self.create_favorites(users, articles)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created:\n'
            f'  - {len(users)} users\n'
            f'  - {len(tags)} tags\n'
            f'  - {len(articles)} articles\n'
            f'  - {options["comments"]} comments\n'
            f'  - Random follows and favorites'
        ))

    def create_users(self, count):
        """Create sample users."""
        users = []
        
        # Predefined users with realistic data
        user_data = [
            {
                'username': 'johndoe',
                'email': 'john@example.com',
                'bio': 'Software developer passionate about clean code and best practices.',
                'image': 'https://api.realworld.io/images/smiley-cyrus.jpg'
            },
            {
                'username': 'janedoe',
                'email': 'jane@example.com',
                'bio': 'Full-stack developer and open source enthusiast.',
                'image': 'https://api.realworld.io/images/smiley-cyrus.jpg'
            },
            {
                'username': 'bobsmith',
                'email': 'bob@example.com',
                'bio': 'Backend engineer specializing in Python and Django.',
                'image': 'https://api.realworld.io/images/smiley-cyrus.jpg'
            },
            {
                'username': 'alicejones',
                'email': 'alice@example.com',
                'bio': 'Frontend developer who loves React and Vue.js.',
                'image': 'https://api.realworld.io/images/smiley-cyrus.jpg'
            },
            {
                'username': 'charliedev',
                'email': 'charlie@example.com',
                'bio': 'DevOps engineer and cloud architecture expert.',
                'image': 'https://api.realworld.io/images/smiley-cyrus.jpg'
            },
            {
                'username': 'evatech',
                'email': 'eva@example.com',
                'bio': 'Machine learning engineer and data scientist.',
                'image': 'https://api.realworld.io/images/smiley-cyrus.jpg'
            },
            {
                'username': 'frankcode',
                'email': 'frank@example.com',
                'bio': 'Mobile developer building iOS and Android apps.',
                'image': 'https://api.realworld.io/images/smiley-cyrus.jpg'
            },
            {
                'username': 'graceful',
                'email': 'grace@example.com',
                'bio': 'UI/UX designer turned frontend developer.',
                'image': 'https://api.realworld.io/images/smiley-cyrus.jpg'
            },
        ]

        for i, data in enumerate(user_data[:count]):
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['username'],
                    'bio': data['bio'],
                    'image': data['image']
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  Created user: {user.username}')
            users.append(user)

        return users

    def create_tags(self):
        """Create sample tags."""
        tag_names = [
            'python', 'django', 'javascript', 'react', 'vue',
            'nodejs', 'typescript', 'docker', 'kubernetes', 'aws',
            'machine-learning', 'data-science', 'devops', 'testing',
            'api', 'rest', 'graphql', 'database', 'postgresql', 'mongodb',
            'tutorial', 'beginner', 'advanced', 'best-practices', 'tips'
        ]

        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(tag=name)
            tags.append(tag)
            if created:
                self.stdout.write(f'  Created tag: {name}')

        return tags

    def create_articles(self, count, users, tags):
        """Create sample articles."""
        articles = []
        
        article_data = [
            {
                'title': 'Getting Started with Django REST Framework',
                'description': 'A comprehensive guide to building APIs with Django REST Framework.',
                'body': '''# Getting Started with Django REST Framework

Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django.

## Installation

```bash
pip install djangorestframework
```

## Creating Your First API

1. Add 'rest_framework' to INSTALLED_APPS
2. Create a serializer
3. Create a view
4. Configure URLs

## Serializers

Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes.

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
```

## Views

DRF provides several view classes to handle API requests.

## Conclusion

Django REST Framework makes it easy to build robust APIs!''',
                'tags': ['django', 'python', 'api', 'rest', 'tutorial']
            },
            {
                'title': 'React Hooks: A Complete Guide',
                'description': 'Learn how to use React Hooks to manage state and side effects.',
                'body': '''# React Hooks: A Complete Guide

React Hooks revolutionized how we write React components.

## useState

The most basic hook for managing state:

```javascript
const [count, setCount] = useState(0);
```

## useEffect

For handling side effects:

```javascript
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);
```

## Custom Hooks

Create reusable logic with custom hooks:

```javascript
function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);
  const increment = () => setCount(c => c + 1);
  const decrement = () => setCount(c => c - 1);
  return { count, increment, decrement };
}
```

## Best Practices

- Always call hooks at the top level
- Only call hooks from React functions
- Use the ESLint plugin for hooks''',
                'tags': ['react', 'javascript', 'tutorial', 'beginner']
            },
            {
                'title': 'Docker for Developers: Essential Commands',
                'description': 'Master the essential Docker commands every developer should know.',
                'body': '''# Docker for Developers

Docker containers have become essential for modern development.

## Basic Commands

### Build an image
```bash
docker build -t myapp .
```

### Run a container
```bash
docker run -d -p 8000:8000 myapp
```

### List containers
```bash
docker ps -a
```

## Docker Compose

For multi-container applications:

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres
```

## Best Practices

1. Use multi-stage builds
2. Minimize layers
3. Use .dockerignore
4. Don't run as root''',
                'tags': ['docker', 'devops', 'tutorial', 'best-practices']
            },
            {
                'title': 'Python Type Hints: A Practical Guide',
                'description': 'Improve your Python code quality with type hints.',
                'body': '''# Python Type Hints

Type hints make Python code more readable and maintainable.

## Basic Syntax

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## Common Types

```python
from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def find_user(user_id: int) -> Optional[User]:
    return User.objects.filter(id=user_id).first()
```

## Benefits

- Better IDE support
- Catch bugs early
- Self-documenting code
- Works with mypy for static analysis''',
                'tags': ['python', 'best-practices', 'tips']
            },
            {
                'title': 'Building RESTful APIs: Design Principles',
                'description': 'Learn the key principles for designing great REST APIs.',
                'body': '''# RESTful API Design Principles

A well-designed API is crucial for developer experience.

## Key Principles

### Use Nouns, Not Verbs
- Good: `/api/articles`
- Bad: `/api/getArticles`

### Use HTTP Methods Correctly
- GET: Retrieve resources
- POST: Create resources
- PUT: Update resources
- DELETE: Remove resources

### Version Your API
```
/api/v1/articles
/api/v2/articles
```

### Use Proper Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Server Error

### Pagination
Always paginate list endpoints:
```json
{
  "articles": [...],
  "articlesCount": 100
}
```''',
                'tags': ['api', 'rest', 'best-practices', 'tutorial']
            },
            {
                'title': 'Introduction to Machine Learning with Python',
                'description': 'Get started with machine learning using Python and scikit-learn.',
                'body': '''# Introduction to Machine Learning

Machine learning is transforming every industry.

## Getting Started

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
```

## Types of ML

1. **Supervised Learning**: Learn from labeled data
2. **Unsupervised Learning**: Find patterns in unlabeled data
3. **Reinforcement Learning**: Learn through trial and error

## Popular Libraries

- scikit-learn
- TensorFlow
- PyTorch
- Keras''',
                'tags': ['machine-learning', 'python', 'data-science', 'beginner']
            },
            {
                'title': 'PostgreSQL Performance Optimization',
                'description': 'Tips and tricks to optimize your PostgreSQL database.',
                'body': '''# PostgreSQL Performance Optimization

Optimize your database for better performance.

## Indexing

```sql
CREATE INDEX idx_articles_author ON articles(author_id);
CREATE INDEX idx_articles_created ON articles(created_at DESC);
```

## Query Analysis

```sql
EXPLAIN ANALYZE SELECT * FROM articles WHERE author_id = 1;
```

## Configuration Tuning

Key settings to consider:
- `shared_buffers`: 25% of RAM
- `work_mem`: 64MB for complex queries
- `effective_cache_size`: 75% of RAM

## Best Practices

1. Use connection pooling
2. Avoid SELECT *
3. Use LIMIT for large tables
4. Regular VACUUM and ANALYZE''',
                'tags': ['postgresql', 'database', 'best-practices', 'advanced']
            },
            {
                'title': 'Vue.js 3 Composition API Tutorial',
                'description': 'Learn the new Composition API in Vue.js 3.',
                'body': '''# Vue.js 3 Composition API

The Composition API provides better code organization.

## Setup Function

```javascript
import { ref, computed, onMounted } from 'vue';

export default {
  setup() {
    const count = ref(0);
    const doubled = computed(() => count.value * 2);
    
    function increment() {
      count.value++;
    }
    
    onMounted(() => {
      console.log('Component mounted');
    });
    
    return { count, doubled, increment };
  }
};
```

## Composables

Create reusable logic:

```javascript
// useCounter.js
export function useCounter() {
  const count = ref(0);
  const increment = () => count.value++;
  return { count, increment };
}
```

## Benefits

- Better TypeScript support
- More flexible code organization
- Easier to share logic between components''',
                'tags': ['vue', 'javascript', 'tutorial']
            },
            {
                'title': 'Kubernetes Basics for Beginners',
                'description': 'Understanding Kubernetes core concepts and components.',
                'body': '''# Kubernetes Basics

Kubernetes orchestrates containerized applications at scale.

## Core Concepts

### Pods
The smallest deployable unit:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: myapp
    image: myapp:1.0
```

### Deployments
Manage replica sets:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
```

### Services
Expose your application:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80
```

## kubectl Commands

```bash
kubectl get pods
kubectl describe pod myapp
kubectl logs myapp
kubectl exec -it myapp -- /bin/bash
```''',
                'tags': ['kubernetes', 'docker', 'devops', 'beginner']
            },
            {
                'title': 'Testing Best Practices in Python',
                'description': 'Write better tests for your Python applications.',
                'body': '''# Testing Best Practices in Python

Good tests are essential for maintainable code.

## pytest Basics

```python
import pytest

def test_addition():
    assert 1 + 1 == 2

def test_exception():
    with pytest.raises(ValueError):
        int("not a number")
```

## Fixtures

```python
@pytest.fixture
def sample_user():
    return User.objects.create(
        username='testuser',
        email='test@example.com'
    )

def test_user_str(sample_user):
    assert str(sample_user) == 'test@example.com'
```

## Mocking

```python
from unittest.mock import patch

@patch('myapp.services.external_api')
def test_with_mock(mock_api):
    mock_api.return_value = {'status': 'ok'}
    result = my_function()
    assert result['status'] == 'ok'
```

## Best Practices

1. Test one thing per test
2. Use descriptive names
3. Arrange-Act-Assert pattern
4. Keep tests fast''',
                'tags': ['python', 'testing', 'best-practices']
            },
        ]

        # Create articles from predefined data
        for i, data in enumerate(article_data[:count]):
            author = random.choice(users)
            article, created = Article.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'body': data['body'],
                    'author': author
                }
            )
            if created:
                # Add tags
                for tag_name in data['tags']:
                    tag = Tag.objects.get(tag=tag_name)
                    article.tags.add(tag)
                self.stdout.write(f'  Created article: {article.title[:50]}...')
            articles.append(article)

        # Create additional random articles if needed
        for i in range(len(article_data), count):
            author = random.choice(users)
            title = f'Article {i + 1}: Exploring New Technologies'
            article, created = Article.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'This is a sample article about various tech topics.',
                    'body': f'# {title}\n\nThis is the body of article {i + 1}.\n\n## Introduction\n\nLorem ipsum dolor sit amet.',
                    'author': author
                }
            )
            if created:
                # Add random tags
                random_tags = random.sample(tags, k=random.randint(1, 4))
                for tag in random_tags:
                    article.tags.add(tag)
                self.stdout.write(f'  Created article: {article.title[:50]}...')
            articles.append(article)

        return articles

    def create_comments(self, count, users, articles):
        """Create sample comments."""
        comment_bodies = [
            'Great article! Very informative.',
            'Thanks for sharing this. Learned something new today.',
            'I have a question about the second point...',
            'This is exactly what I was looking for!',
            'Well written and easy to understand.',
            'Could you elaborate more on this topic?',
            'I disagree with some points, but overall good read.',
            'Bookmarked for future reference!',
            'This helped me solve a problem I had for weeks.',
            'Looking forward to more articles like this.',
            'The code examples are very helpful.',
            'I tried this approach and it works great!',
            'Nice explanation of complex concepts.',
            'Would love to see a follow-up article.',
            'This is a must-read for beginners.',
        ]

        for i in range(count):
            article = random.choice(articles)
            author = random.choice(users)
            body = random.choice(comment_bodies)
            
            Comment.objects.create(
                body=body,
                author=author,
                article=article
            )
        
        self.stdout.write(f'  Created {count} comments')

    def create_follows(self, users):
        """Create random follow relationships."""
        for user in users:
            # Each user follows 1-3 random other users
            other_users = [u for u in users if u != user]
            follows = random.sample(other_users, k=min(random.randint(1, 3), len(other_users)))
            for followed in follows:
                user.follow(followed)
        
        self.stdout.write('  Created follow relationships')

    def create_favorites(self, users, articles):
        """Create random favorites."""
        for user in users:
            # Each user favorites 2-5 random articles
            favorites = random.sample(articles, k=min(random.randint(2, 5), len(articles)))
            for article in favorites:
                article.favorited_by.add(user)
        
        self.stdout.write('  Created favorites')
