# Runway Navigator - Godmode Dashboard

A modern SaaS dashboard application featuring an interactive 3D globe view for market intelligence and vendor management.

## 🌟 Features

### Core Dashboard
- **KPI Monitoring**: Real-time tracking of runway months, cash on hand, and monthly burn
- **Navigation**: Sidebar with Dashboard, Signals, Vendors, Actions, and Settings
- **Responsive Design**: Modern UI built with TailwindCSS

### Godmode Globe View
- **3D Interactive Globe**: Powered by 21st.dev globe component
- **Company Points**: Visual representation of companies across the globe
- **Risk Assessment**: Color-coded points based on risk levels (low/medium/high)
- **Interactive Elements**: Click points to view detailed company information
- **Real-time Data**: Live transaction feed and market signals

### Company Intelligence
- **Detailed Profiles**: Company information, market cap, employees, founding date
- **Market Signals**: Positive, negative, and neutral signals with severity ratings
- **Transaction History**: Recent deals, investments, and partnerships
- **Risk Analysis**: Comprehensive risk assessment and monitoring

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd runway-navigator
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

## 🏗️ Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── layout/         # Layout components (Sidebar, Header)
│   ├── dashboard/      # Dashboard-specific components
│   ├── globe/          # Globe view components
│   └── ui/             # Generic UI components
├── pages/              # Page components
├── store/              # State management (Zustand)
├── types/              # TypeScript type definitions
├── data/               # Mock data and fixtures
├── styles/             # Global styles and TailwindCSS
└── utils/              # Utility functions
```

## 🎯 Key Components

### GlobeView
The main 3D globe component that integrates with 21st.dev globe library:
- Interactive 3D globe with company points
- Click interactions for company selection
- Hover effects and animations
- Fallback mode for development

### CompanyDrawer
Right-side panel showing detailed company information:
- Company metrics and details
- Market signals and risk assessment
- Transaction history
- Interactive elements

### TransactionOverlay
Left-side panel displaying recent market activity:
- Real-time transaction feed
- Deal types and amounts
- Status indicators
- Time-based filtering

## 🎨 UI/UX Features

- **Dark Theme**: Professional dark color scheme
- **Glassmorphism**: Modern backdrop blur effects
- **Smooth Animations**: CSS transitions and hover effects
- **Responsive Design**: Mobile-friendly layout
- **Interactive Elements**: Hover states and click feedback

## 🔧 Configuration

### Globe Settings
- Background color customization
- Point size and resolution
- Auto-rotation controls
- Animation speed settings

### Theme Customization
- TailwindCSS configuration
- Custom color palette
- Animation keyframes
- Component-specific styles

## 📊 Data Models

### Company
```typescript
interface Company {
  id: string;
  name: string;
  coordinates: { lat: number; lng: number };
  marketCap?: number;
  industry: string;
  signals: Signal[];
  riskLevel: 'low' | 'medium' | 'high';
  // ... additional fields
}
```

### Signal
```typescript
interface Signal {
  id: string;
  type: 'positive' | 'negative' | 'neutral';
  category: 'financial' | 'operational' | 'market' | 'regulatory';
  severity: 1 | 2 | 3 | 4 | 5;
  // ... additional fields
}
```

## 🚧 Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Adding New Features
1. Create component in appropriate directory
2. Add TypeScript interfaces
3. Update state management if needed
4. Style with TailwindCSS classes
5. Test interactions and responsiveness

## 🔮 Future Enhancements

### Phase 2
- Real-time data integration
- Advanced filtering and search
- User authentication
- Custom dashboards

### Phase 3
- Machine learning insights
- Predictive analytics
- Advanced reporting
- API integrations

## 🐛 Troubleshooting

### Common Issues

**Globe not loading**
- Check browser console for errors
- Verify @21st/globe package installation
- Ensure WebGL support is enabled

**Styling issues**
- Verify TailwindCSS is properly configured
- Check CSS import order
- Clear browser cache

**Performance issues**
- Reduce number of company points
- Optimize globe rendering settings
- Use React.memo for heavy components

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or support, please open an issue in the repository or contact the development team.

---

**Built with ❤️ using React, TypeScript, TailwindCSS, and 21st.dev Globe**
