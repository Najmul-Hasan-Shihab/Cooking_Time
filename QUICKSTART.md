# 🎉 Phase 0 Complete - Quick Start Guide

## What We Built

✅ **Complete Development Environment for Recipe Website**

### Project Structure
```
Recipe_website/
├── backend/              # Django REST API
│   ├── config/          # Django settings
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── venv/            # Python virtual environment
├── frontend/            # React + Vite
│   ├── src/
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile.dev
├── .github/workflows/   # CI/CD pipeline
├── docker-compose.yml
├── .env
└── Documentation (README, CODESTYLE, CONTRIBUTING)
```

## 🚀 Running the Application

### Option 1: Local Development (Current Setup)

#### Backend (Django API)
```powershell
cd backend
d:\Personal\Front-end\Recipe_website\backend\venv\Scripts\python.exe manage.py runserver
```
- API will be available at: **http://localhost:8000**
- Health check: **http://localhost:8000/api/health/**
- API root: **http://localhost:8000/api/**

#### Frontend (React)
```powershell
cd frontend
npm run dev
```
- App will be available at: **http://localhost:5173**

### Option 2: Docker (Recommended for Full Stack)

**Note:** MongoDB needs to be running for the backend to connect properly.

```powershell
# Start all services
docker-compose up

# Or start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **MongoDB:** localhost:27017

## 📝 Current API Endpoints

### Health Check
```
GET http://localhost:8000/api/health/
```
Response:
```json
{
  "status": "healthy",
  "message": "Recipe Website API is running",
  "version": "0.1.0",
  "phase": "Phase 0 - Development Environment Ready"
}
```

### API Root
```
GET http://localhost:8000/api/
```

## ✅ Phase 0 Checkpoint - Verification

Verify your setup is working:

1. **Django Backend**
   - [ ] Server starts without errors
   - [ ] Can access http://localhost:8000/api/
   - [ ] Health endpoint returns "healthy" status

2. **React Frontend**
   - [ ] npm install completes successfully
   - [ ] Dev server starts at http://localhost:5173
   - [ ] Welcome page displays

3. **MongoDB** (for Docker setup)
   - [ ] Container is healthy
   - [ ] Backend can connect to MongoDB

## 🔧 Common Commands

### Backend
```powershell
cd backend

# Activate virtual environment (if needed)
.\venv\Scripts\Activate.ps1

# Run migrations
d:\Personal\Front-end\Recipe_website\backend\venv\Scripts\python.exe manage.py migrate

# Create superuser
d:\Personal\Front-end\Recipe_website\backend\venv\Scripts\python.exe manage.py createsuperuser

# Run server
d:\Personal\Front-end\Recipe_website\backend\venv\Scripts\python.exe manage.py runserver
```

### Frontend
```powershell
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Type check
npm run type-check
```

### Docker
```powershell
# Build images
docker-compose build

# Start services
docker-compose up

# Restart a specific service
docker-compose restart backend

# View logs for a service
docker-compose logs -f backend

# Execute commands in containers
docker-compose exec backend python manage.py migrate
docker-compose exec frontend npm run build

# Stop and remove containers
docker-compose down

# Remove volumes too (clean slate)
docker-compose down -v
```

## 📦 What's Configured

### Backend
- ✅ Django 5.2.8
- ✅ Django REST Framework
- ✅ MongoEngine (MongoDB ODM)
- ✅ JWT Authentication (SimpleJWT)
- ✅ CORS Headers
- ✅ Environment variable management

### Frontend
- ✅ React 18
- ✅ Vite (build tool)
- ✅ TypeScript
- ✅ TailwindCSS
- ✅ React Router
- ✅ React Query (for API calls)
- ✅ Zustand (state management)
- ✅ Hot Module Replacement

### DevOps
- ✅ Docker & Docker Compose
- ✅ GitHub Actions CI
- ✅ Environment configuration
- ✅ Git setup with .gitignore

## 🎯 Next Steps - Phase 1

Ready to build the core API? Phase 1 includes:

1. **MongoDB Collections & Models**
   - Users (with gamification fields)
   - Recipes (with all metadata)
   - Comments
   - User Actions
   - Badges

2. **Authentication System**
   - User registration
   - Login with JWT
   - Token refresh
   - Protected endpoints

3. **Recipe CRUD API**
   - Create recipes (with image upload)
   - List recipes (with filtering)
   - Get recipe details
   - Update/delete recipes
   - Basic search

4. **Checkpoint Deliverable**
   - Create user account
   - Login and get JWT token
   - Create a recipe with images
   - List and view recipes

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F
```

### Frontend won't start
```powershell
# Clear node_modules and reinstall
Remove-Item -Recurse -Force node_modules
npm install
```

### MongoDB connection errors
- Ensure MongoDB is running (docker-compose up mongodb)
- Check connection details in `.env`
- For local setup: update MONGODB_HOST=localhost in `.env`

### Import errors in VS Code
This is normal - VS Code doesn't recognize the virtual environment yet. The code will run fine.

To fix:
1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose the venv interpreter: `.\backend\venv\Scripts\python.exe`

## 📚 Resources

- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [React Docs](https://react.dev/)
- [Vite Docs](https://vitejs.dev/)
- [TailwindCSS Docs](https://tailwindcss.com/)
- [MongoEngine Docs](http://mongoengine.org/)

---

**🎊 Congratulations! Phase 0 is complete. Your development environment is ready!**

Ready to start Phase 1? Just let me know! 🚀
