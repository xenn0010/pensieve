# 🧠 Pensieve + Runway Navigator

> **Palantir for Startups** - Enterprise-grade data intelligence platform with interactive 3D dashboard

Pensieve transforms how startups harness their data through powerful analytics, predictive modeling, and actionable insights - all accessible via simple API keys. Now enhanced with **Runway Navigator**, an interactive 3D globe dashboard for market intelligence and vendor management.

## 🚀 What is Pensieve?

Pensieve is an enterprise-grade data intelligence platform designed specifically for startups. Think of it as having Palantir's analytical capabilities without the enterprise complexity. We provide:

- **🔍 Advanced Data Analytics** - Uncover hidden patterns in your business data
- **📊 Predictive Modeling** - Forecast trends and identify opportunities
- **🎯 Actionable Insights** - Turn data into strategic decisions
- **🔐 Simple API Access** - Get started in minutes with API keys
- **📈 Scalable Infrastructure** - Grows with your startup
- **🌍 Interactive 3D Dashboard** - Visual market intelligence with Runway Navigator

## 🌟 Runway Navigator Features

### Core Dashboard
- **KPI Monitoring**: Real-time tracking of runway months, cash on hand, and monthly burn
- **Navigation**: Sidebar with Dashboard, Chessboard, Vendors, and Settings
- **Responsive Design**: Modern UI built with TailwindCSS

### Godmode Globe View
- **3D Interactive Globe**: Powered by react-globe.gl
- **Company Points**: Visual representation of companies across the globe
- **Risk Assessment**: Color-coded points based on risk levels (low/medium/high)
- **Interactive Elements**: Click points to view detailed company information
- **Real-time Data**: Live transaction feed and market signals

### Financial Scenario Planning (Chessboard)
- **Interactive Grid**: Build and compare financial scenarios
- **Move Library**: Pre-built financial actions and strategies
- **Visual Comparison**: Charts and tables for scenario analysis
- **AI Recommendations**: Intelligent move suggestions

### Company Intelligence
- **Detailed Profiles**: Company information, market cap, employees, founding date
- **Market Signals**: Positive, negative, and neutral signals with severity ratings
- **Transaction History**: Recent deals, investments, and partnerships
- **Risk Analysis**: Comprehensive risk assessment and monitoring

## 🛠️ Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Python 3.8+ (for backend services)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/xenn0010/pensieve.git
   cd pensieve
   git checkout runway-navigator
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 🏗️ Project Structure

```
├── Frontend (Runway Navigator)
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── layout/         # Layout components (Sidebar, Header)
│   │   │   ├── dashboard/      # Dashboard-specific components
│   │   │   ├── globe/          # Globe view components
│   │   │   ├── chessboard/     # Financial scenario planning
│   │   │   └── ui/             # Generic UI components
│   │   ├── pages/              # Page components
│   │   ├── store/              # State management (Zustand)
│   │   ├── types/              # TypeScript type definitions
│   │   ├── data/               # Mock data and fixtures
│   │   └── styles/             # Global styles and TailwindCSS
│   └── package.json
│
├── Backend (Pensieve Core)
│   ├── intelligence-engine/     # AI and decision orchestration
│   ├── mcp-servers/            # Model Context Protocol servers
│   ├── data-pipeline/          # Data processing and analytics
│   ├── database/               # Database schemas and setup
│   ├── config/                 # Configuration and settings
│   └── tests/                  # Test suites
│
└── Documentation
    ├── API_DOCUMENTATION.md    # API reference
    ├── docs/                   # Detailed documentation
    └── README.md               # This file
```

## 🎯 Key Components

### GlobeView
The main 3D globe component that integrates with react-globe.gl:
- Interactive 3D globe with company points
- Click interactions for company selection
- Hover effects and animations
- Intelligent search and filtering

### CompanyDrawer
Right-side panel showing detailed company information:
- Company metrics and details
- Market signals and risk assessment
- Transaction history
- Interactive elements with expand/collapse

### TransactionOverlay
Left-side panel displaying recent market activity:
- Real-time transaction feed
- Deal types and amounts
- Status indicators
- Time-based filtering

### Chessboard
Financial scenario planning interface:
- Interactive grid for building scenarios
- Move library with pre-built strategies
- Visual comparison tools
- AI-powered recommendations

## 🎨 UI/UX Features

- **Dark Theme**: Professional dark color scheme
- **Glassmorphism**: Modern backdrop blur effects
- **Smooth Animations**: CSS transitions and hover effects
- **Responsive Design**: Mobile-friendly layout
- **Interactive Elements**: Hover states and click feedback
- **Professional Charts**: Recharts integration for data visualization

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
- Real-time data integration with Pensieve backend
- Advanced filtering and search
- User authentication
- Custom dashboards

### Phase 3
- Machine learning insights from Pensieve
- Predictive analytics
- Advanced reporting
- API integrations

## 🐛 Troubleshooting

### Common Issues

**Globe not loading**
- Check browser console for errors
- Verify react-globe.gl package installation
- Ensure WebGL support is enabled

**Styling issues**
- Verify TailwindCSS is properly configured
- Check CSS import order
- Clear browser cache

**Performance issues**
- Reduce number of company points
- Optimize globe rendering settings
- Use React.memo for heavy components

## 📚 API Reference

### Authentication

All API requests require your API key in the header:

```bash
Authorization: Bearer YOUR_API_KEY
```

### Rate Limits

- **Free Tier**: 1,000 requests/month
- **Starter**: 10,000 requests/month
- **Growth**: 100,000 requests/month
- **Scale**: Custom limits

### Endpoints

#### Analytics
- `POST /v1/analytics/analyze` - Run custom analysis
- `GET /v1/analytics/dashboard` - Get dashboard data
- `POST /v1/analytics/report` - Generate custom reports

#### Predictions
- `POST /v1/predictions/forecast` - Generate forecasts
- `POST /v1/predictions/segment` - Customer segmentation
- `GET /v1/predictions/models` - Available ML models

#### Data
- `POST /v1/data/upload` - Upload datasets
- `GET /v1/data/sources` - List data sources
- `DELETE /v1/data/sources/{id}` - Remove data source

## 💰 Pricing

| Plan | Price | API Calls | Features |
|------|-------|-----------|----------|
| **Free** | $0/month | 1K/month | Basic analytics, 3 dashboards |
| **Starter** | $99/month | 10K/month | Advanced analytics, ML models |
| **Growth** | $299/month | 100K/month | Custom models, priority support |
| **Scale** | Custom | Custom | Enterprise features, dedicated support |

## 🔒 Security & Compliance

- **SOC 2 Type II** certified
- **GDPR** compliant
- **HIPAA** ready (enterprise plans)
- **End-to-end encryption** for data in transit and at rest
- **Regular security audits** and penetration testing

## 🆘 Support

- **Documentation**: [docs.pensieve.ai](https://docs.pensieve.ai)
- **Community**: [community.pensieve.ai](https://community.pensieve.ai)
- **Email**: support@pensieve.ai
- **Slack**: [Join our community](https://slack.pensieve.ai)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with ❤️ for the startup community. Special thanks to our early adopters and beta testers.

---

**Ready to unlock your data's potential?** [Get started with Pensieve today](https://pensieve.ai/signup)

*Pensieve - Where data becomes intelligence*

**Runway Navigator - Visual market intelligence meets financial planning**
