# Alejandria Frontend

React frontend for Alejandria document management system.

## Tech Stack

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Zustand** - State management
- **Axios** - HTTP client
- **TailwindCSS** - Styling
- **shadcn/ui** - UI components
- **Storybook** - Component development

## Prerequisites

- Node.js 20+
- npm or yarn

## Installation

```bash
# Install dependencies
npm install
```

## Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

See `.env.example` for reference.

## Development

```bash
# Start development server (http://localhost:3000)
npm run dev

# Run linting
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format
```

## Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Storybook

```bash
# Start Storybook (http://localhost:6006)
npm run storybook

# Build Storybook
npm run build-storybook
```

## Docker

```bash
# Build and run with docker-compose
docker-compose --profile frontend up --build

# Access frontend at http://localhost:3000
```

## Project Structure

```
src/
├── components/     # React components
│   ├── layout/     # Layout components
│   └── ui/         # shadcn/ui components
├── pages/          # Page components
├── services/       # API services
├── stores/         # Zustand stores
├── types/          # TypeScript types
├── utils.ts        # Utility functions
├── App.tsx         # Main app component
└── main.tsx        # Entry point
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint issues
- `npm run format` - Format code with Prettier
- `npm run storybook` - Start Storybook
- `npm run build-storybook` - Build Storybook
