# Phase 0 Setup Complete! 🎉

Congratulations! You've completed Phase 0 of the Recipe Website project.

## ✅ What We've Built

### Project Structure
- ✅ Monorepo with `/backend` and `/frontend` directories
- ✅ Documentation (README, CODESTYLE, CONTRIBUTING)
- ✅ Git configuration (.gitignore)

### Backend Setup
- ✅ Django project structure
- ✅ Dockerfile for containerization
- ✅ requirements.txt with all dependencies
- ✅ Ready for Django REST Framework + MongoEngine

### Frontend Setup
- ✅ React + Vite + TypeScript configuration
- ✅ TailwindCSS setup
- ✅ Basic App component
- ✅ Dockerfile for development

### DevOps
- ✅ docker-compose.yml for all services (Django, MongoDB, React)
- ✅ Environment configuration (.env.example)
- ✅ GitHub Actions CI pipeline

## 🚀 Next Steps - Initialize the Project

### Step 1: Copy Environment Variables
```powershell
cd d:\Personal\Front-end\Recipe_website
Copy-Item .env.example .env
```

Edit `.env` and update the secrets:
- `SECRET_KEY` - Generate a new Django secret key
- `JWT_SECRET_KEY` - Generate a JWT secret
- `MONGODB_PASSWORD` - Set a strong password

### Step 2: Install Frontend Dependencies
```powershell
cd frontend
npm install
```

### Step 3: Initialize Django Project
We need to create the Django project inside the backend folder:

```powershell
cd ..\backend
python -m venv venv
.\venv\Scripts\activate
pip install django djangorestframework mongoengine
django-admin startproject config .
```

### Step 4: Test with Docker (Recommended)
Once Django is initialized:

```powershell
cd ..
docker-compose up
```

This will start:
- MongoDB on port 27017
- Django API on http://localhost:8000
- React app on http://localhost:5173

## 📋 Phase 0 Checkpoint Verification

Before moving to Phase 1, verify:

- [ ] `docker-compose up` runs without errors
- [ ] MongoDB container is healthy
- [ ] Django backend starts and responds at http://localhost:8000
- [ ] React frontend loads at http://localhost:5173
- [ ] Empty DRF API root (/api/) is accessible

## 🎯 Phase 1 Preview - Data Model & Core API

Next, we'll build:
1. MongoDB collections (users, recipes, comments, etc.)
2. MongoEngine models
3. JWT authentication endpoints
4. Recipe CRUD API
5. Basic user registration and login

## 💡 Tips

### Generate Django Secret Key
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Access MongoDB Shell
```powershell
docker exec -it recipe_mongodb mongosh -u recipe_admin -p change-this-password
```

### View Logs
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## ❓ Troubleshooting

### Port Already in Use
If ports 8000, 5173, or 27017 are in use:
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process by PID
taskkill /PID <process_id> /F
```

### Docker Issues
```powershell
# Rebuild containers
docker-compose up --build

# Clean restart
docker-compose down -v
docker-compose up
```

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [MongoEngine Documentation](http://mongoengine.org/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)

---

**Ready to start Phase 1?** Let me know and we'll begin building the data models and authentication system! 🚀
