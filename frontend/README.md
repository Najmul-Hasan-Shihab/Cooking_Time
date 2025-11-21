# Recipe Website Frontend

Modern React application with Vite, TypeScript, and TailwindCSS.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **TypeScript** - Type safety
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Zustand** - State management
- **Axios** - HTTP client
- **React Query** - Server state management

## Project Structure

```
frontend/
├── src/
│   ├── api/           # API client functions
│   ├── assets/        # Static assets (images, fonts)
│   ├── components/    # Reusable components
│   │   ├── common/    # Common UI components
│   │   ├── recipes/   # Recipe-specific components
│   │   ├── auth/      # Authentication components
│   │   └── layout/    # Layout components
│   ├── hooks/         # Custom React hooks
│   ├── pages/         # Page components
│   ├── store/         # State management
│   ├── types/         # TypeScript type definitions
│   ├── utils/         # Utility functions
│   ├── App.tsx        # Main App component
│   └── main.tsx       # Entry point
├── public/            # Public static files
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

## Getting Started

### Local Development

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

4. Preview production build:
```bash
npm run preview
```

### Docker Development

```bash
docker-compose up frontend
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler check
- `npm test` - Run tests

## Key Features

### Phase 0-2
- Responsive card grid layout
- Recipe detail view
- User authentication
- Search and filters

### Phase 3+
- XP and badge system
- Profile dashboard
- Interactive cooking mode
- Social features (follow, comments)
- Personalized recommendations

## Environment Variables

Create a `.env.local` file:

```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Recipe Website
```

## Code Style

- Use functional components with hooks
- TypeScript for type safety
- TailwindCSS for styling
- Follow ESLint and Prettier rules

See [CODESTYLE.md](../CODESTYLE.md) for detailed guidelines.
