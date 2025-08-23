# 🚀 Pensieve + Runway Navigator Integration Guide

## 📋 Overview

This document outlines the technical steps to integrate the **Pensieve backend** (enterprise data intelligence platform) with the **Runway Navigator frontend** (interactive 3D dashboard) into a fully functional system.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Runway Navigator)                 │
├─────────────────────────────────────────────────────────────────┤
│  React App (Vite) │ 3D Globe │ Chessboard │ Dashboard │ UI   │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/WebSocket
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend (Pensieve)                          │
├─────────────────────────────────────────────────────────────────┤
│ Frontend API │ Intelligence Engine │ MCP Servers │ Data Layer  │
└─────────────────────┬───────────────────────────────────────────┘
                      │ External APIs
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                  External Services                              │
├─────────────────────────────────────────────────────────────────┤
│ Brex API │ SixtyFour API │ MixRank API │ Supabase │ Redis     │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Prerequisites

### Required Software
- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **Redis** (local or cloud)
- **PostgreSQL** (via Supabase)

### API Keys Required
- **Gemini API Key** (Google AI)
- **Supabase URL & Key**
- **Redis URL**
- **Brex API Key** (optional)
- **SixtyFour API Key** (optional)
- **MixRank API Key** (optional)

## 📁 Project Structure

```
pensieve/
├── Frontend (Runway Navigator)
│   ├── src/
│   │   ├── components/          # UI Components
│   │   ├── pages/              # Page Components
│   │   ├── store/              # State Management
│   │   └── types/              # TypeScript Types
│   ├── package.json            # Frontend Dependencies
│   └── vite.config.ts          # Build Configuration
│
├── Backend (Pensieve Core)
│   ├── intelligence-engine/     # AI & Decision Engine
│   ├── mcp-servers/            # External API Servers
│   ├── data-pipeline/          # Data Processing
│   ├── config/                 # Configuration
│   └── main.py                 # Main Server
│
└── Integration Files
    ├── .env                    # Environment Variables
    ├── requirements.txt        # Python Dependencies
    └── INTEGRATION_GUIDE.md    # This Document
```

## 🚀 Step 1: Backend Setup

### 1.1 Install Python Dependencies
```bash
# Navigate to project root
cd /path/to/pensieve

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python --version
pip list | grep fastapi
```

### 1.2 Environment Configuration
Create `.env` file in project root:
```bash
# Core Configuration
APP_NAME=Pensieve_CIO
DEBUG=true

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
REDIS_URL=redis://localhost:6379

# Optional External APIs
BREX_API_KEY=your_brex_api_key_here
SIXTYFOUR_API_KEY=your_sixtyfour_api_key_here
MIXRANK_API_KEY=your_mixrank_api_key_here

# Demo Mode (for testing)
USE_MOCK_DATA=true
DEMO_FINANCIAL_PROFILE=healthy_saas
```

### 1.3 Start Backend Services
```bash
# Start Redis (if local)
redis-server

# Start Frontend API Server
python frontend_api.py

# Verify server is running
curl http://localhost:8001/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-XX...",
  "version": "1.0.0"
}
```

## 🎨 Step 2: Frontend Setup

### 2.1 Install Node Dependencies
```bash
# Navigate to project root
cd /path/to/pensieve

# Install frontend dependencies
npm install

# Verify installation
npm list react react-globe.gl
```

### 2.2 Frontend Configuration
Update `src/config/api.ts` (create if doesn't exist):
```typescript
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8001',
  ENDPOINTS: {
    HEALTH: '/health',
    DASHBOARD: '/dashboard/overview',
    COMPANY_RESEARCH: '/research/company',
    AGENT_QUERY: '/agent/query',
    INTELLIGENCE: '/intelligence/signals',
    ACTIONS: '/actions/recent'
  },
  WEBSOCKET_URL: 'ws://localhost:8001/ws'
};
```

### 2.3 Start Frontend Development Server
```bash
# Start development server
npm run dev

# Verify frontend is running
# Open http://localhost:3000 in browser
```

## 🔗 Step 3: API Integration

### 3.1 Replace Mock Data with Real API Calls

#### Update Company Data Source
**File:** `src/data/mockCompanies.ts`
```typescript
import { API_CONFIG } from '../config/api';

export const fetchRealCompanyData = async () => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/intelligence/companies`);
    const data = await response.json();
    return data.companies;
  } catch (error) {
    console.error('Failed to fetch company data:', error);
    return mockCompanies; // Fallback to mock data
  }
};
```

#### Update Transaction Data Source
**File:** `src/data/mockTransactions.ts`
```typescript
import { API_CONFIG } from '../config/api';

export const fetchRealTransactionData = async () => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/intelligence/transactions`);
    const data = await response.json();
    return data.transactions;
  } catch (error) {
    console.error('Failed to fetch transaction data:', error);
    return mockTransactions; // Fallback to mock data
  }
};
```

### 3.2 Integrate Dashboard KPIs
**File:** `src/components/dashboard/KPICards.tsx`
```typescript
import { useEffect, useState } from 'react';
import { API_CONFIG } from '../../config/api';

export const KPICards = () => {
  const [kpiData, setKpiData] = useState(null);

  useEffect(() => {
    const fetchKPIData = async () => {
      try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/dashboard/metrics`);
        const data = await response.json();
        setKpiData(data);
      } catch (error) {
        console.error('Failed to fetch KPI data:', error);
      }
    };

    fetchKPIData();
    const interval = setInterval(fetchKPIData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  // ... rest of component
};
```

### 3.3 Integrate Company Intelligence
**File:** `src/components/globe/CompanyDrawer.tsx`
```typescript
import { API_CONFIG } from '../../config/api';

const fetchCompanyIntelligence = async (companyId: string) => {
  try {
    const response = await fetch(
      `${API_CONFIG.BASE_URL}/intelligence/company/${companyId}`
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch company intelligence:', error);
    return null;
  }
};
```

## 🌐 Step 4: Real-time Integration

### 4.1 WebSocket Connection Setup
**File:** `src/hooks/useWebSocket.ts`
```typescript
import { useEffect, useRef, useState } from 'react';
import { API_CONFIG } from '../config/api';

export const useWebSocket = () => {
  const ws = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [data, setData] = useState(null);

  useEffect(() => {
    ws.current = new WebSocket(API_CONFIG.WEBSOCKET_URL);

    ws.current.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setData(message);
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    };

    return () => {
      ws.current?.close();
    };
  }, []);

  return { isConnected, data };
};
```

### 4.2 Real-time Dashboard Updates
**File:** `src/components/dashboard/Dashboard.tsx`
```typescript
import { useWebSocket } from '../../hooks/useWebSocket';

export const Dashboard = () => {
  const { isConnected, data } = useWebSocket();

  useEffect(() => {
    if (data && data.type === 'dashboard_update') {
      // Update dashboard with real-time data
      updateDashboardData(data.payload);
    }
  }, [data]);

  // ... rest of component
};
```

## 🎯 Step 5: Feature Integration

### 5.1 Globe Intelligence Integration
**File:** `src/components/globe/GlobeView.tsx`
```typescript
import { API_CONFIG } from '../../config/api';

const fetchGlobeIntelligence = async () => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/intelligence/globe`);
    const data = await response.json();
    return data.companies;
  } catch (error) {
    console.error('Failed to fetch globe intelligence:', error);
    return [];
  }
};

const handleCompanyClick = async (companyId: string) => {
  try {
    const response = await fetch(
      `${API_CONFIG.BASE_URL}/intelligence/company/${companyId}`
    );
    const companyData = await response.json();
    setSelectedCompany(companyData);
  } catch (error) {
    console.error('Failed to fetch company details:', error);
  }
};
```

### 5.2 Chessboard Financial Integration
**File:** `src/components/chessboard/EnhancedChessboardGrid.tsx`
```typescript
import { API_CONFIG } from '../../config/api';

const fetchFinancialScenarios = async () => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/financial/scenarios`);
    const data = await response.json();
    return data.scenarios;
  } catch (error) {
    console.error('Failed to fetch financial scenarios:', error);
    return [];
  }
};

const getAIMoveRecommendations = async (currentState: any) => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/agent/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: 'Recommend next financial move',
        context: { current_state: currentState }
      })
    });
    const data = await response.json();
    return data.recommendations;
  } catch (error) {
    console.error('Failed to get AI recommendations:', error);
    return [];
  }
};
```

### 5.3 Search and Intelligence
**File:** `src/components/globe/FooterSearchBar.tsx`
```typescript
import { API_CONFIG } from '../../config/api';

const performIntelligentSearch = async (query: string) => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/intelligence/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Search failed:', error);
    return [];
  }
};
```

## 🔍 Step 6: Testing & Validation

### 6.1 API Endpoint Testing
```bash
# Test health endpoint
curl http://localhost:8001/health

# Test dashboard endpoint
curl http://localhost:8001/dashboard/overview

# Test company research
curl -X POST "http://localhost:8001/research/company" \
  -H "Content-Type: application/json" \
  -d '{"company_domain": "anthropic.com", "research_depth": "standard"}'
```

### 6.2 Frontend Integration Testing
1. **Open Dashboard** - Verify KPIs load from API
2. **Navigate to Globe** - Check company data loads
3. **Click Company Points** - Verify intelligence data displays
4. **Use Search Bar** - Test intelligent search functionality
5. **Open Chessboard** - Verify financial data integration

### 6.3 Real-time Testing
1. **Monitor WebSocket Connection** - Check browser console
2. **Test Data Updates** - Verify real-time dashboard updates
3. **Check Error Handling** - Test fallback to mock data

## 🚧 Step 7: Error Handling & Fallbacks

### 7.1 API Error Handling
```typescript
const apiCall = async (endpoint: string, options = {}) => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, options);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    
    // Return mock data as fallback
    return getMockDataForEndpoint(endpoint);
  }
};
```

### 7.2 Connection Status Monitoring
```typescript
const useConnectionStatus = () => {
  const [isBackendConnected, setIsBackendConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/health`);
        setIsBackendConnected(response.ok);
      } catch (error) {
        setIsBackendConnected(false);
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 10000);
    return () => clearInterval(interval);
  }, []);

  return isBackendConnected;
};
```

## 📊 Step 8: Performance Optimization

### 8.1 Data Caching Strategy
```typescript
const useCachedData = (key: string, fetchFunction: () => Promise<any>) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const cached = localStorage.getItem(key);
    if (cached) {
      setData(JSON.parse(cached));
      setLoading(false);
    }

    fetchFunction().then(freshData => {
      setData(freshData);
      localStorage.setItem(key, JSON.stringify(freshData));
      setLoading(false);
    });
  }, [key]);

  return { data, loading };
};
```

### 8.2 Lazy Loading Components
```typescript
// Lazy load heavy components
const GlobeView = lazy(() => import('./globe/GlobeView'));
const Chessboard = lazy(() => import('./chessboard/Chessboard'));

// Use Suspense for loading states
<Suspense fallback={<div>Loading...</div>}>
  <GlobeView />
</Suspense>
```

## 🚀 Step 9: Production Deployment

### 9.1 Environment Configuration
```bash
# Production .env
APP_NAME=Pensieve_CIO
DEBUG=false
USE_MOCK_DATA=false

# Production API keys
GEMINI_API_KEY=prod_key_here
SUPABASE_URL=prod_url_here
SUPABASE_KEY=prod_key_here
REDIS_URL=prod_redis_url_here
```

### 9.2 Build and Deploy
```bash
# Build frontend
npm run build

# Start production backend
python main.py

# Serve frontend (using nginx, etc.)
# Configure reverse proxy to backend API
```

## 🔧 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep fastapi

# Check environment variables
echo $GEMINI_API_KEY
```

#### Frontend Can't Connect to Backend
```bash
# Check CORS configuration
# Verify backend is running on correct port
# Check network tab in browser dev tools
```

#### Data Not Loading
```bash
# Check API endpoints
curl http://localhost:8001/health

# Check browser console for errors
# Verify API keys are set correctly
```

## 📈 Monitoring & Maintenance

### 9.1 Health Checks
- **Backend Health**: `/health` endpoint
- **Database Status**: Supabase connection monitoring
- **API Performance**: Response time monitoring
- **Error Rates**: Log analysis and alerting

### 9.2 Logging
```typescript
// Frontend logging
const logEvent = (event: string, data: any) => {
  console.log(`[${new Date().toISOString()}] ${event}:`, data);
  
  // Send to backend logging service
  fetch(`${API_CONFIG.BASE_URL}/logs/frontend`, {
    method: 'POST',
    body: JSON.stringify({ event, data, timestamp: Date.now() })
  });
};
```

## 🎯 Success Criteria

### Integration Complete When:
- ✅ Frontend loads real data from backend APIs
- ✅ Real-time updates work via WebSocket
- ✅ Error handling gracefully falls back to mock data
- ✅ All features (Globe, Chessboard, Dashboard) functional
- ✅ Performance meets requirements (<2s load time)
- ✅ Error rate <1% for critical operations

## 📚 Next Steps

1. **Complete Integration** - Follow steps 1-9 above
2. **User Testing** - Validate all features work together
3. **Performance Tuning** - Optimize based on real usage
4. **Feature Expansion** - Add new AI-powered capabilities
5. **Production Deployment** - Deploy to production environment

---

**Document Version:** 1.0  
**Last Updated:** January 2025  
**Maintainer:** Development Team  

For questions or issues, refer to the troubleshooting section or contact the development team.
