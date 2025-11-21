# Django Backend for Recipe Website

## Structure

```
backend/
├── config/              # Django project settings
├── apps/
│   ├── authentication/  # User auth & JWT
│   ├── recipes/         # Recipe models & APIs
│   ├── users/           # User profiles & gamification
│   ├── comments/        # Comment system
│   └── gamification/    # XP, badges, challenges
├── manage.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Setup

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

### Docker Development

```bash
docker-compose up backend
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT tokens
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout

### Recipes
- `GET /api/recipes/` - List recipes (with filters)
- `GET /api/recipes/:slug/` - Get recipe detail
- `POST /api/recipes/` - Create recipe (auth required)
- `PUT /api/recipes/:id/` - Update recipe (author only)
- `DELETE /api/recipes/:id/` - Delete recipe (admin only)
- `POST /api/recipes/:id/mark_cooked/` - Mark as cooked

### Users
- `GET /api/users/:id/` - Get user profile
- `GET /api/users/:id/stats/` - Get user stats (XP, badges)
- `POST /api/users/:id/follow/` - Follow user

### Search
- `GET /api/search/?q=&tags=&difficulty=` - Search recipes
- `POST /api/search/by_ingredients/` - Search by ingredients

## Testing

```bash
python manage.py test
```

## Environment Variables

See `.env.example` in root directory.
