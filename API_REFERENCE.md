# Recipe Website - API Reference

Base URL: `http://localhost:8000`

## Authentication Endpoints

### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response (201 Created)**:
```json
{
  "user": {
    "id": "string",
    "username": "string",
    "email": "string",
    "xp": 0,
    "level": 1,
    "badges": [],
    "created_at": "ISO8601"
  },
  "access": "JWT_TOKEN",
  "refresh": "REFRESH_TOKEN"
}
```

---

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": "string",
    "username": "string",
    "email": "string",
    "xp": 0,
    "level": 1,
    "badges": []
  },
  "access": "JWT_TOKEN",
  "refresh": "REFRESH_TOKEN"
}
```

---

### Get Current User
```http
GET /api/auth/me/
Authorization: Bearer <JWT_TOKEN>
```

**Response (200 OK)**:
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "avatar_url": "string",
  "bio": "string",
  "xp": 110,
  "level": 2,
  "badges": ["badge_id_1", "badge_id_2"],
  "followers_count": 0,
  "following_count": 0,
  "preferences": {
    "cuisines": [],
    "dietary_restrictions": [],
    "favorite_tags": []
  },
  "created_at": "ISO8601"
}
```

---

### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "REFRESH_TOKEN"
}
```

**Response (200 OK)**:
```json
{
  "access": "NEW_JWT_TOKEN"
}
```

---

### Logout
```http
POST /api/auth/logout/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "refresh": "REFRESH_TOKEN"
}
```

**Response (200 OK)**:
```json
{
  "message": "Logout successful"
}
```

---

## Recipe Endpoints

### List Recipes
```http
GET /api/recipes/
```

**Query Parameters**:
- `tags`: Filter by tags (multiple allowed)
- `difficulty`: Filter by difficulty (`easy`, `medium`, `hard`)
- `cuisine`: Filter by cuisine (case-insensitive contains)
- `time_max`: Maximum total time in minutes
- `q`: Search query (searches in title)
- `sort`: Sort order (`created_at`, `-created_at`, `views`, `-views`, `rating_stats.average`, `-rating_stats.average`)
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Example**:
```
GET /api/recipes/?tags=dessert&tags=chocolate&difficulty=easy&sort=-views
```

**Response (200 OK)**:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/recipes/?page=2",
  "previous": null,
  "results": [
    {
      "id": "string",
      "title": "string",
      "slug": "string",
      "description": "string",
      "images": ["url1", "url2"],
      "prep_time": 15,
      "cook_time": 30,
      "total_time": 45,
      "servings": 4,
      "difficulty": "easy",
      "tags": ["tag1", "tag2"],
      "cuisine": "Italian",
      "rating_stats": {
        "average": 4.5,
        "count": 10
      },
      "views": 100,
      "cook_count": 20,
      "rarity": "common",
      "author": {
        "id": "string",
        "username": "string",
        "avatar_url": "string",
        "level": 2
      },
      "created_at": "ISO8601"
    }
  ]
}
```

---

### Create Recipe
```http
POST /api/recipes/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Perfect Chocolate Chip Cookies",
  "description": "The ultimate cookie recipe",
  "difficulty": "easy",
  "prep_time": 15,
  "cook_time": 12,
  "servings": 24,
  "tags": ["dessert", "cookies", "chocolate"],
  "cuisine": "American",
  "ingredients": [
    {
      "name": "All-purpose flour",
      "quantity": "2 1/4",
      "unit": "cups",
      "optional": false
    },
    {
      "name": "Chocolate chips",
      "quantity": "2",
      "unit": "cups",
      "optional": false
    }
  ],
  "steps": [
    {
      "step_number": 1,
      "text": "Preheat oven to 375F",
      "step_time": 5
    },
    {
      "step_number": 2,
      "text": "Mix ingredients",
      "step_time": 10
    }
  ],
  "images": ["http://example.com/image.jpg"],
  "nutrition_info": {
    "calories": 150,
    "protein": 2,
    "carbs": 20,
    "fat": 7,
    "fiber": 1,
    "sugar": 10
  }
}
```

**Response (201 Created)**:
```json
{
  "id": "string",
  "title": "Perfect Chocolate Chip Cookies",
  "slug": "perfect-chocolate-chip-cookies",
  "description": "The ultimate cookie recipe",
  "images": ["http://example.com/image.jpg"],
  "ingredients": [...],
  "steps": [...],
  "prep_time": 15,
  "cook_time": 12,
  "total_time": 27,
  "servings": 24,
  "difficulty": "easy",
  "tags": ["dessert", "cookies", "chocolate"],
  "categories": [],
  "cuisine": "American",
  "rating_stats": {
    "average": 0.0,
    "count": 0
  },
  "views": 0,
  "cook_count": 0,
  "rarity": "common",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "is_published": false,
  "is_featured": false,
  "author": {
    "id": "string",
    "username": "string",
    "avatar_url": "",
    "level": 1
  }
}
```

**Note**: Creating a recipe awards **+50 XP** to the author.

---

### Get Recipe Detail
```http
GET /api/recipes/{slug}/
```

**Example**:
```
GET /api/recipes/perfect-chocolate-chip-cookies/
```

**Response (200 OK)**:
```json
{
  "id": "string",
  "title": "Perfect Chocolate Chip Cookies",
  "slug": "perfect-chocolate-chip-cookies",
  "description": "The ultimate cookie recipe",
  "images": ["http://example.com/image.jpg"],
  "ingredients": [
    {
      "name": "All-purpose flour",
      "quantity": "2 1/4",
      "unit": "cups",
      "optional": false
    }
  ],
  "steps": [
    {
      "step_number": 1,
      "text": "Preheat oven to 375F",
      "image": "",
      "step_time": 5
    }
  ],
  "prep_time": 15,
  "cook_time": 12,
  "total_time": 27,
  "servings": 24,
  "difficulty": "easy",
  "tags": ["dessert", "cookies", "chocolate"],
  "categories": [],
  "cuisine": "American",
  "nutrition_info": {
    "calories": 150,
    "protein": 2,
    "carbs": 20,
    "fat": 7,
    "fiber": 1,
    "sugar": 10
  },
  "rating_stats": {
    "average": 0.0,
    "count": 0
  },
  "views": 1,
  "cook_count": 0,
  "rarity": "common",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "is_published": false,
  "is_featured": false,
  "author": {
    "id": "string",
    "username": "testchef",
    "avatar_url": "",
    "level": 1
  }
}
```

**Note**: Each GET request increments the `views` counter.

---

### Update Recipe
```http
PUT /api/recipes/{slug}/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description",
  ...
}
```

**Response (200 OK)**: Same as recipe detail.

**Permissions**: Only the recipe author can update.

---

### Delete Recipe
```http
DELETE /api/recipes/{slug}/
Authorization: Bearer <JWT_TOKEN>
```

**Response (204 No Content)**

**Permissions**: Only the recipe author can delete.

---

### Mark Recipe as Cooked
```http
POST /api/recipes/{slug}/mark_cooked/
Authorization: Bearer <JWT_TOKEN>
```

**Example**:
```
POST /api/recipes/perfect-chocolate-chip-cookies/mark_cooked/
```

**Response (200 OK)**:
```json
{
  "message": "Recipe marked as cooked",
  "xp_awarded": 10,
  "user": {
    "xp": 60,
    "level": 1
  }
}
```

**Note**: Awards **+10 XP** to the user and increments recipe's `cook_count`.

---

### Search Recipes
```http
GET /api/recipes/search/
```

**Query Parameters**:
- `q`: Search query (searches in title, description, tags)

**Example**:
```
GET /api/recipes/search/?q=chocolate
```

**Response (200 OK)**: Same format as List Recipes.

---

## Gamification System

### XP Rewards
| Action | XP Reward |
|--------|-----------|
| Submit Recipe | +50 XP |
| Mark as Cooked | +10 XP |
| Comment | +5 XP |
| Rate Recipe | +3 XP |
| Follow User | +2 XP |
| Share Recipe | +5 XP |
| Daily Login | +1 XP |

### Level Thresholds
| Level | XP Required |
|-------|-------------|
| 1 | 0 |
| 2 | 100 |
| 3 | 300 |
| 4 | 600 |
| 5 | 1,000 |
| 6 | 1,500 |
| 7 | 2,100 |
| 8 | 2,800 |
| 9 | 3,600 |
| 10 | 4,500 |
| 11+ | +1,000 per level |

### Recipe Rarity
| Rarity | Cook Count |
|--------|------------|
| common | 0-99 |
| uncommon | 100-999 |
| rare | 1,000-9,999 |
| legendary | 10,000+ |

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## PowerShell Testing Examples

### Register & Login
```powershell
# Register
$register = @{
    username = "testuser"
    email = "test@example.com"
    password = "password123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri http://localhost:8000/api/auth/register/ `
    -Method POST -Body $register -ContentType "application/json"

# Save token
$global:accessToken = $response.access

# Login
$login = @{
    username = "testuser"
    password = "password123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri http://localhost:8000/api/auth/login/ `
    -Method POST -Body $login -ContentType "application/json"

$global:accessToken = $response.access
```

### Create Recipe
```powershell
$recipe = @{
    title = "My Recipe"
    description = "A delicious recipe"
    difficulty = "easy"
    prep_time = 10
    cook_time = 20
    servings = 4
    tags = @("tag1", "tag2")
    cuisine = "Italian"
    ingredients = @(
        @{ name = "Ingredient 1"; quantity = "1"; unit = "cup" }
    )
    steps = @(
        @{ step_number = 1; text = "Do this"; step_time = 5 }
    )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri http://localhost:8000/api/recipes/ `
    -Method POST `
    -Body ([System.Text.Encoding]::UTF8.GetBytes($recipe)) `
    -ContentType "application/json; charset=utf-8" `
    -Headers @{ "Authorization" = "Bearer $global:accessToken" }
```

### Get User Profile
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/auth/me/ `
    -Method GET `
    -Headers @{ "Authorization" = "Bearer $global:accessToken" }
```

### Mark Recipe as Cooked
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/recipes/my-recipe/mark_cooked/ `
    -Method POST `
    -Headers @{ "Authorization" = "Bearer $global:accessToken" }
```

---

**Last Updated**: November 21, 2025
