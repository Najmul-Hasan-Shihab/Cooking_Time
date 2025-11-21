# Recipe Website - Gamified Cooking Platform

A modern, gamified recipe sharing platform with Django backend, MongoDB, and React frontend.

## 🎯 Project Overview

This platform combines recipe sharing with gaming mechanics, allowing users to:
- Discover and share recipes with a collectible card-style UI
- Earn XP and badges through cooking and community engagement
- Follow other cooks and build a cooking community
- Get personalized recipe recommendations
- Use interactive cooking mode with step-by-step guidance

## 🏗️ Architecture

- **Backend**: Django + Django REST Framework + MongoEngine
- **Database**: MongoDB
- **Frontend**: React + Vite + TypeScript + TailwindCSS
- **Deployment**: Docker + Docker Compose

## 📁 Project Structure

```
Recipe_website/
├── backend/          # Django REST API
├── frontend/         # React + Vite app
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Setup with Docker

1. Clone the repository
2. Copy environment file:
   ```bash
   cp .env.example .env
   ```
3. Start all services:
   ```bash
   docker-compose up
   ```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- MongoDB: localhost:27017

## 📚 Documentation

- [Code Style Guide](CODESTYLE.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [API Documentation](backend/docs/API.md)

## 🎮 Key Features

### Phase 0 ✅ (Current)
- [x] Project structure setup
- [x] Docker development environment
- [ ] CI/CD pipeline

### Phase 1 (Planned)
- Data models for users, recipes, comments
- JWT authentication
- Basic CRUD API for recipes

### Future Phases
- Gamification (XP, badges, levels)
- Community features (comments, follows)
- Personalization & recommendations
- Interactive cooking mode
- Admin dashboard

## 🧪 Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

## 📝 License

MIT License

## 👥 Contributors

Built with ❤️ by the Recipe Website team
