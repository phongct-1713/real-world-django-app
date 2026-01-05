# Real World Django App
## Project Structure

```
real-world-django-app/
├── conduit/              # Main project configuration
│   ├── settings.py       # Django settings with JWT config
│   ├── urls.py           # Root URL routing
│   └── exceptions.py     # Custom exception handler
├── users/                # User/Auth app
│   ├── models.py         # Custom User model with JWT token generation
│   ├── serializers.py    # Registration, Login, User serializers
│   ├── views.py          # Auth views (register, login, user CRUD)
│   ├── authentication.py # Custom JWT authentication class
│   └── urls.py
├── profiles/             # Profiles app
│   ├── serializers.py    # Profile serializer
│   ├── views.py          # Profile & Follow views
│   └── urls.py
├── articles/             # Articles/Comments/Tags app
│   ├── models.py         # Article, Comment, Tag models
│   ├── serializers.py    # Article, Comment serializers
│   ├── views.py          # CRUD views for articles, comments, tags
│   └── urls.py
├── requirements.txt
├── manage.py
└── README.md
```

## Endpoints
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/users/` | Register |
| POST | `/api/users/login/` | Login |
| GET | `/api/user/` | Get current user |
| PUT | `/api/user/` | Update user |
| GET | `/api/profiles/:username/` | Get profile |
| POST | `/api/profiles/:username/follow/` | Follow user |
| DELETE | `/api/profiles/:username/follow/` | Unfollow user |
| GET | `/api/articles/` | List articles (with filters) |
| GET | `/api/articles/feed/` | Feed from followed users |
| POST | `/api/articles/` | Create article |
| GET | `/api/articles/:slug/` | Get article |
| PUT | `/api/articles/:slug/` | Update article |
| DELETE | `/api/articles/:slug/` | Delete article |
| POST | `/api/articles/:slug/favorite/` | Favorite article |
| DELETE | `/api/articles/:slug/favorite/` | Unfavorite article |
| GET | `/api/articles/:slug/comments/` | Get comments |
| POST | `/api/articles/:slug/comments/` | Create comment |
| DELETE | `/api/articles/:slug/comments/:id/` | Delete comment |
| GET | `/api/tags/` | List all tags |