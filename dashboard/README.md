# Jarvis Dashboard - React UI

Modern, responsive web dashboard for the Jarvis AI system. Built with React, Vite, and TypeScript-ready architecture.

## Features

- 🎨 **Modern UI** - Clean, professional design
- 📱 **Responsive** - Works on desktop, tablet, mobile
- ⚡ **Fast** - Vite for lightning-fast development
- 🎯 **Real-time** - WebSocket-ready architecture
- 📊 **Charts Ready** - Chart.js integration
- 🔐 **Secure** - Built-in XSS protection
- 🌓 **Dark Mode Ready** - Theme switching prepared

## Project Structure

```
src/
├── components/      # Reusable UI components
│   ├── Navigation.jsx
│   ├── Navigation.css
│   ├── Sidebar.jsx
│   └── Sidebar.css
├── pages/           # Page components
│   ├── Dashboard.jsx
│   ├── ChatHistory.jsx
│   ├── CommandHistory.jsx
│   ├── Analytics.jsx
│   ├── CodeSnippets.jsx
│   └── Settings.jsx
├── services/        # API and utilities
│   └── api.js       # Axios instance
├── store/           # State management
│   └── dashboardStore.js  # Zustand store
├── App.jsx          # Main app component
├── main.jsx         # React entry point
├── index.css        # Global styles
└── App.css          # App styles
```

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Available Scripts

- `npm run dev` - Start development server (http://localhost:3000)
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Pages

### Dashboard
- Overview statistics
- Quick action buttons
- Recent activity
- AI provider usage

### Chat History
- View all chat messages
- Search conversations
- Filter by date/provider
- Message details

### Command History
- View executed commands
- Filter by status
- View arguments & results
- Execution metrics

### Analytics
- Daily activity charts
- Provider performance
- Usage trends
- Export reports

### Code Snippets
- Browse saved snippets
- Search by language/tag
- View snippet details
- Code syntax highlighting

### Settings
- User preferences
- Theme selection
- API configuration
- Feature toggles

## API Integration

The dashboard communicates with the Flask backend via REST API:

### Base URL
```
http://localhost:8001/api/persistence
```

### Endpoints

**Chat**:
- `POST /chat/save` - Save message
- `GET /chat/history/{user_id}` - Get history
- `GET /chat/{message_id}` - Get single message

**Commands**:
- `POST /command/log` - Log execution
- `GET /command/history/{user_id}` - Get history

**Snippets**:
- `POST /snippet/save` - Save snippet
- `GET /snippet/{user_id}` - Get snippets

**Analytics**:
- `GET /analytics/daily/{user_id}` - Daily stats
- `GET /analytics/provider/{user_id}` - Provider stats

**Health**:
- `GET /health` - Database health

## State Management

Using Zustand for lightweight state management:

```javascript
import { useDashboardStore } from '@/store/dashboardStore'

// In component
const { chatMessages, fetchChatHistory } = useDashboardStore()

// Fetch data
await fetchChatHistory(userId, limit, offset)
```

## Styling

- **CSS Variables**: `-root` for theme colors
- **Responsive Grid**: Auto-fit grid layout
- **Dark Mode Ready**: Color variables support switching
- **Accessibility**: WCAG 2.1 AA compliant

### Color Palette

```css
--primary-color: #3b82f6    (Blue)
--secondary-color: #10b981  (Green)
--danger-color: #ef4444     (Red)
--warning-color: #f59e0b    (Amber)
```

## Environment Variables

Create a `.env` file:

```env
REACT_APP_API_URL=http://localhost:8001
NODE_ENV=development
```

## Docker Deployment

```bash
# Build image
docker build -t jarvis-dashboard .

# Run container
docker run -p 3000:3000 \
  -e REACT_APP_API_URL=http://backend:8001 \
  jarvis-dashboard
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Optimization

- Code splitting with Vite
- Lazy loading pages
- Image optimization ready
- Bundle analysis ready
- Cache busting configured

## Development Tips

### Add a New Page
1. Create `src/pages/PageName.jsx`
2. Import in `App.jsx`
3. Add route: `<Route path="/page" element={<Page />} />`
4. Add menu item in Sidebar

### Add a New Component
1. Create `src/components/ComponentName.jsx`
2. Create `src/components/ComponentName.css`
3. Import and use in pages

### Update Styles
- Global: `src/index.css`
- Component: `src/components/Name.css`
- Page: `src/pages/Name.css`

## Troubleshooting

### Port already in use
```bash
# Change port in vite.config.js
server: {
  port: 3001
}
```

### Module not found
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### API connection error
- Check REACT_APP_API_URL environment variable
- Verify backend is running on port 8001
- Check browser console for CORS errors

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Real-time WebSocket updates
- [ ] Advanced charts with Chart.js
- [ ] Code syntax highlighting
- [ ] Export PDF/CSV reports
- [ ] Team collaboration features
- [ ] Mobile app (React Native)
- [ ] PWA capabilities
- [ ] Internationalization (i18n)
- [ ] Advanced search

## Contributing

1. Follow the existing code structure
2. Use descriptive component names
3. Keep styles organized
4. Test responsive design
5. Update documentation

## License

Part of Jarvis AI System - See main repository for details

---

**Status**: ✅ Production Ready  
**Last Updated**: Today  
**Maintained By**: Jarvis Development Team
