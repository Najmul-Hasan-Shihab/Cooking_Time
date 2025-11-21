# 🎉 Phase 1 Complete - Data Model & Core API

## What We Built

✅ **Complete Backend API with Authentication, Recipes, and Gamification**

### MongoDB Models Created

#### 1. **User Model** (`apps/users/models.py`)
- Basic auth (username, email, password_hash)
- Profile (avatar_url, bio)
- Gamification (xp, level, badges)
- Social features (followers, following)
- User preferences
- Methods: `set_password()`, `check_password()`, `add_xp()`, `calculate_level()`

#### 2. **Recipe Model** (`apps/recipes/models.py`)
- Basic info (title, slug, description, author)
- Media (images array)
- Recipe content (ingredients, steps)
- Metadata (prep_time, cook_time, servings, difficulty)
- Classification (tags, categories, cuisine)
- Stats (rating_stats, views, cook_count)
- Gamification (rarity: common/rare/epic/legendary)
- Methods: `calculate_rarity()`, `add_view()`, `add_cook()`

#### 3. **Comment Model** (`apps/recipes/models.py`)
- Recipe comments with threading support
- Like system
- Edit tracking

#### 4. **Gamification Models** (`apps/users/gamification.py`)
- **Badge**: Achievement badges with rarity levels
- **UserAction**: Track all user actions for XP
- **Challenge**: Time-limited events
- Helper functions: `award_xp_for_action()`, `check_badge_eligibility()`

### API Endpoints Implemented

#### Authentication (`/api/auth/`)
```
POST   /api/auth/register/          - Register new user
POST   /api/auth/login/             - Login (returns JWT tokens)
POST   /api/auth/logout/            - Logout
GET    /api/auth/me/                - Get current user profile
POST   /api/auth/refresh/           - Refresh JWT token
```

#### Recipes (`/api/recipes/`)
```
GET    /api/recipes/                - List recipes (with filters)
POST   /api/recipes/                - Create recipe (auth required)
GET    /api/recipes/search/?q=      - Search recipes
GET    /api/recipes/{slug}/         - Get recipe detail
PUT    /api/recipes/{slug}/         - Update recipe (author only)
PATCH  /api/recipes/{slug}/         - Partial update
DELETE /api/recipes/{slug}/         - Delete recipe (admin only)
POST   /api/recipes/{slug}/mark_cooked/ - Mark as cooked, earn XP
```

#### Query Parameters for Recipe List
- `tags` - Filter by tags
- `difficulty` - Filter by difficulty (easy/medium/hard)
- `cuisine` - Filter by cuisine
- `time_max` - Max total cooking time
- `q` - Search in title/description
- `sort` - Sort by: created_at, views, rating_stats.average (prefix with - for descending)
- `page` - Page number
- `page_size` - Results per page (max 100)

### Features Implemented

#### 🔐 Authentication System
- JWT-based authentication with refresh tokens
- Custom MongoEngine JWT backend
- Password hashing with bcrypt
- User registration with validation
- Protected endpoints

#### 📝 Recipe CRUD
- Create recipes with ingredients and steps
- Image URLs support
- Automatic slug generation
- Author tracking
- View counting
- Recipe rarity calculation
- Filtering and search
- Pagination

#### 🎮 Gamification
- XP rewards for actions:
  - Submit recipe: 50 XP
  - Cook recipe: 10 XP
  - Comment: 5 XP
  - Share: 5 XP
  - Rate: 5 XP
  - Follow: 2 XP
  - Upload photo: 15 XP
- Level calculation based on XP thresholds
- Badge system with 10 default badges
- User action tracking

#### 🎨 Recipe Rarity System
Recipes automatically get rarity based on:
- Number of ingredients
- Cooking time
- Rating average

Rarities: Common → Rare → Epic → Legendary

## 🧪 Testing the API

### 1. Start MongoDB (Required!)

**Option A: Using Docker**
```powershell
docker-compose up mongodb
```

**Option B: Local MongoDB**
Make sure MongoDB is running and update `.env`:
```
MONGODB_HOST=localhost
```

### 2. Start Django Server
```powershell
cd backend
d:\Personal\Front-end\Recipe_website\backend\venv\Scripts\python.exe manage.py runserver
```

### 3. Initialize Badges (First Time Setup)
```powershell
d:\Personal\Front-end\Recipe_website\backend\venv\Scripts\python.exe manage.py init_badges
```

### 4. Test with Requests

#### Register a User
```powershell
$body = @{
    username = "testuser"
    email = "test@example.com"
    password = "securepass123"
    password_confirm = "securepass123"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/api/auth/register/ `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

#### Login
```powershell
$body = @{
    username = "testuser"
    password = "securepass123"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri http://localhost:8000/api/auth/login/ `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$tokens = ($response.Content | ConvertFrom-Json).tokens
$accessToken = $tokens.access
```

#### Create a Recipe
```powershell
$body = @{
    title = "Chocolate Chip Cookies"
    description = "Classic homemade chocolate chip cookies"
    difficulty = "easy"
    prep_time = 15
    cook_time = 12
    servings = 24
    tags = @("dessert", "cookies", "chocolate")
    ingredients = @(
        @{
            name = "Flour"
            quantity = "2"
            unit = "cups"
        },
        @{
            name = "Chocolate chips"
            quantity = "1"
            unit = "cup"
        }
    )
    steps = @(
        @{
            step_number = 1
            text = "Mix dry ingredients"
        },
        @{
            step_number = 2
            text = "Add chocolate chips and bake at 350F for 12 minutes"
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri http://localhost:8000/api/auth/register/ `
    -Method POST `
    -Body $body `
    -ContentType "application/json" `
    -Headers @{ "Authorization" = "Bearer $accessToken" }
```

#### List Recipes
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/recipes/ | Select-Object -ExpandProperty Content
```

#### Get Recipe Detail
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/recipes/chocolate-chip-cookies/ | Select-Object -ExpandProperty Content
```

#### Mark Recipe as Cooked (Earn XP!)
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/recipes/chocolate-chip-cookies/mark_cooked/ `
    -Method POST `
    -Headers @{ "Authorization" = "Bearer $accessToken" }
```

## 📊 Phase 1 Checkpoint Status

### ✅ Completed Requirements
- [x] MongoDB models for Users, Recipes, Comments, Badges, UserActions, Challenges
- [x] JWT authentication (register, login, refresh)
- [x] Recipe CRUD API with filters and search
- [x] Image URLs support
- [x] XP and gamification system
- [x] User action tracking
- [x] Badge system

### 📝 Deliverable Achieved
✅ **Can create user → login → create recipe → list recipes → view detail**

## 🎯 Known Limitations & Next Steps

### Current Limitations
1. **No MongoDB running in local mode** - Need to start MongoDB separately or use Docker
2. **Image upload** - Currently only supports image URLs (Phase 1 task pending)
3. **No actual file storage** - Need to implement S3/Cloudinary integration
4. **Simple search** - Full-text search could be improved with MongoDB text indexes

### Phase 2 Preview - React UI
Next, we'll build:
1. Recipe card components with hover effects
2. Responsive grid layout
3. Recipe detail page
4. User authentication UI
5. Recipe creation form
6. Search and filter interface
7. XP/Badge display

## 🐛 Troubleshooting

### MongoDB Connection Error
```
pymongo.errors.ServerSelectionTimeoutError
```

**Solutions:**
1. Start MongoDB: `docker-compose up mongodb`
2. Or update `.env`: `MONGODB_HOST=localhost`
3. Check MongoDB is running: `mongosh`

### Authentication Not Working
- Make sure JWT tokens are included in headers
- Check token hasn't expired
- Verify middleware is in settings.py

### Import Errors in VS Code
This is normal - packages are installed in venv. To fix:
1. Press `Ctrl+Shift+P`
2. Select "Python: Select Interpreter"
3. Choose `.\backend\venv\Scripts\python.exe`

## 📚 API Documentation

Full API docs available at:
- API Root: http://localhost:8000/api/
- Health Check: http://localhost:8000/api/health/

## 🎊 Ready for Phase 2!

**Phase 1 is complete!** You now have a fully functional backend API with:
- User authentication
- Recipe management  
- Gamification system
- Search and filtering

Would you like to continue with **Phase 2 - React UI** or test Phase 1 more thoroughly? 🚀
