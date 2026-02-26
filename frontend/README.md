# 💻 Jarvis Brain Frontend

Modern React UI for AI-powered code evolution.

## 📋 Requirements

- Node.js 18+
- npm or yarn

## 🔧 Installation

```bash
# Install dependencies
npm install

# Start development server
npm start

# Opens http://localhost:3000
```

## 🏗️ Project Structure

```
src/
├── App.jsx           # Main component
├── App.css          # Styling
├── index.jsx        # Entry point
└── components/      # Reusable components (future)
```

## 🎨 Features

### Chat Interface
- Real-time messaging with Jarvis Bot
- Command support (analyze, suggestions, help)
- Conversation history display
- Message typing indicator

### Analysis Dashboard
- AI backend status display
- Quick action buttons
- Project statistics

### History Viewer
- Past improvement records
- Timestamp tracking
- Statistics breakdown

### Settings Panel
- Configuration display
- Environment settings
- Feature toggles

## 🚀 Build

```bash
# Development build
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

## 📱 Responsive Design

- Mobile-first approach
- Flexbox layout
- Responsive font sizes
- Touch-friendly buttons

## 🎯 Usage

1. **Chat Tab** (Default)
   - Type questions or commands
   - Use quick command buttons
   - View conversation history

2. **Analysis Tab**
   - Check AI backend status
   - Trigger project scan
   - View quick stats

3. **History Tab**
   - See past improvements
   - Track progress over time
   - View statistics

4. **Settings Tab**
   - Review configuration
   - View feature status

## 🔌 API Integration

Connects to backend at `REACT_APP_API_URL` (default: `http://localhost:5000/api`)

Endpoints used:
- `POST /api/chat/message` - Send chat message
- `POST /api/evolve/analyze` - Scan project
- `POST /api/evolve/file` - Analyze file
- `GET /api/evolve/suggestions` - Get suggestions
- `GET /api/history/improvements` - Get history
- `GET /api/config/get` - Get configuration
- `GET /api/ai/status` - Check AI status

## 🎨 Styling

- Dark theme with gradient accents
- Cyan (#00d4ff) and lime (#00ff88) colors
- Smooth transitions
- Glassmorphism effects
- Modern gradient backgrounds

## 📚 Component Breakdown

### Main App Component
- State management with React Hooks
- Tab navigation
- Message handling
- API integration

### Chat Container
- Message display
- Input area
- Quick command buttons
- Auto-scroll

### Analysis Container
- Status cards
- Quick action buttons
- AI service monitor

### History Container
- Timeline view
- Record display
- Statistics

### Settings Container
- Configuration display
- JSON viewer

## 🧪 Development

```bash
# Start with hot reload
npm start

# Run tests (if configured)
npm test

# Build for production
npm run build
```

## 📦 Dependencies

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "axios": "^1.6.0",
  "react-icons": "^4.12.0",
  "tailwindcss": "^3.3.0",
  "react-router-dom": "^6.20.0"
}
```

## 🌐 Environment Variables

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=1.0.0
```

## 🐛 Debugging

1. Open browser DevTools (F12)
2. Check Console for errors
3. Check Network tab for API calls
4. Verify API is running on port 5000

## 🚨 Common Issues

### "Cannot connect to API"
- Check if backend is running: `curl http://localhost:5000/api/health`
- Verify `REACT_APP_API_URL` in environment
- Check CORS settings in backend

### Chat not responding
- Check browser console for errors
- Verify backend is running
- Check if Ollama is running (for AI features)

### Frontend not loading
- Clear browser cache
- Run `npm install` again
- Check Node.js version (18+)

## 🔄 TypeScript Version

To use TypeScript instead of JSX:

```bash
# Install TypeScript
npm install --save-dev typescript @types/react @types/react-dom

# Rename files
mv src/App.jsx src/App.tsx
mv src/index.jsx src/index.tsx

# Create tsconfig.json
npx tsc --init
```

## 🎯 Future Enhancements

- [ ] Component library (Storybook)
- [ ] Unit tests (Jest)
- [ ] E2E tests (Cypress)
- [ ] Dark/Light theme toggle
- [ ] Code syntax highlighting
- [ ] Real-time notifications
- [ ] Multi-file upload
- [ ] Export results

## 🚀 Deployment

### Vercel
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Docker
```bash
docker build -t jarvis-frontend .
docker run -p 3000:3000 jarvis-frontend
```

## 📄 License

MIT License

---

**Built with React + ⚡ Vite**
