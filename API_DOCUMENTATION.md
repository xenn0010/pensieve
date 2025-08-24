# Pensieve Frontend API Documentation

## Overview

The Pensieve Frontend API provides comprehensive endpoints for building intelligent business dashboards and interfaces. This API exposes the autonomous agent's capabilities, intelligence data, and real-time insights for frontend visualization and interaction.

**Base URL:** `http://localhost:8001`  
**API Version:** 1.0.0  
**Content-Type:** `application/json`

---

## Quick Start

### 1. Start the API Server
```bash
cd /path/to/pensieve
python frontend_api.py
```

### 2. Basic Health Check
```bash
curl http://localhost:8001/health
```

### 3. Research a Company
```bash
curl -X POST "http://localhost:8001/research/company" \
  -H "Content-Type: application/json" \
  -d '{
    "company_domain": "anthropic.com",
    "research_depth": "standard",
    "include_competitors": true
  }'
```

---

## Endpoint Categories

### 🏠 Dashboard Endpoints
Get overview data and metrics for main dashboard

### 🔍 Research Endpoints  
Research companies and analyze competitors

### 🤖 Agent Endpoints
Query the autonomous agent and get capabilities

### 📊 Intelligence Endpoints
Access market insights and intelligence signals

### ⚡ Action Endpoints
View executed actions and performance analytics

### 📈 Real-time Endpoints
Get live system status and metrics

---

## Dashboard Endpoints

### GET `/dashboard/overview`
Get comprehensive dashboard overview data

**Response Model:** `DashboardDataResponse`
```json
{
  "total_companies_analyzed": 15,
  "active_intelligence_signals": 12,
  "actions_executed_today": 24,
  "cache_hit_rate": 0.85,
  "top_insights": [
    {
      "title": "Competitor Distress Detected",
      "company": "TechCorp Inc",
      "impact": "High",
      "confidence": 0.87
    }
  ],
  "recent_actions": [
    {
      "action": "talent_poaching",
      "target": "competitor-xyz.com", 
      "status": "completed",
      "impact": "$450K talent value"
    }
  ]
}
```

### GET `/dashboard/metrics`
Get real-time system metrics for widgets

**Response:**
```json
{
  "system_status": "operational",
  "agent_health": 98.5,
  "api_response_time": 245,
  "intelligence_sources": {
    "sixtyfour": {"status": "connected", "last_call": "2 minutes ago"},
    "mixrank": {"status": "connected", "last_call": "5 minutes ago"},
    "brex": {"status": "simulated", "last_call": "1 minute ago"},
    "pylon": {"status": "connected", "last_call": "3 minutes ago"}
  },
  "cache_stats": {
    "total_entries": 23,
    "hit_rate": 0.85,
    "avg_response_time": "1.2s"
  }
}
```

---

## Research Endpoints

### POST `/research/company`
Research a company using real intelligence APIs

**Request Model:** `CompanyResearchRequest`
```json
{
  "company_domain": "anthropic.com",
  "research_depth": "standard",
  "include_competitors": true
}
```

**Response Model:** `CompanyIntelligenceResponse`
```json
{
  "company": "anthropic.com",
  "financial_health": "strong",
  "employee_count": 250,
  "technology_stack": ["Claude API", "Mobile App", "Web Platform"],
  "risk_factors": ["Regulatory scrutiny", "Market competition"],
  "opportunities": ["Enterprise expansion", "International growth"],
  "competitive_position": "leading",
  "intelligence_confidence": 0.85,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

### GET `/research/companies`
Get list of previously researched companies

**Response:**
```json
{
  "companies": ["anthropic.com", "openai.com", "google.com"],
  "total": 3,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

### GET `/research/company/{company_domain}/competitors`
Get competitor analysis for a specific company

**Path Parameters:**
- `company_domain` (string): Company domain to analyze

**Response:**
```json
{
  "target_company": "anthropic.com",
  "competitors": [
    {
      "company": "openai.com",
      "similarity_score": 0.85,
      "financial_health": "stable", 
      "threat_level": "high",
      "opportunities": ["talent_acquisition", "market_share_capture"]
    }
  ],
  "analysis_date": "2024-01-15T10:30:00Z"
}
```

---

## Agent Endpoints

### POST `/agent/query`
Ask the autonomous agent a question

**Request Model:** `AgentQueryRequest`
```json
{
  "query": "What should we do about the competitor showing distress signals?",
  "context": {"company": "anthropic.com"},
  "company_focus": "anthropic.com"
}
```

**Response:**
```json
{
  "query": "What should we do about the competitor showing distress signals?",
  "response": "Based on the intelligence signals indicating competitor distress, I recommend executing a three-pronged approach: 1) Launch talent poaching campaigns targeting their senior engineers and product managers, 2) Evaluate acquisition opportunities while their valuation is depressed, 3) Shift market positioning to capture the market share gap they're leaving behind...",
  "suggested_actions": [
    "talent_poaching",
    "acquisition_evaluation", 
    "competitive_intelligence_gathering",
    "market_positioning_shift"
  ],
  "confidence": 0.85,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET `/agent/capabilities`
Get comprehensive agent capabilities by category

**Response:**
```json
{
  "total_actions": 40,
  "categories": {
    "financial_actions": {
      "count": 8,
      "actions": [
        "Emergency Cash Management",
        "Expense Optimization",
        "Funding Preparation",
        "..."
      ]
    },
    "competitive_actions": {
      "count": 8, 
      "actions": [
        "Talent Poaching",
        "Acquisition Evaluation",
        "..."
      ]
    }
  },
  "intelligence_sources": ["SixtyFour", "MixRank", "Brex", "Pylon"],
  "autonomous_execution": true
}
```

---

## Intelligence Endpoints

### GET `/intelligence/insights`
Get current market insights and intelligence signals

**Response Model:** `List[MarketInsightResponse]`
```json
[
  {
    "insight_type": "competitor_distress",
    "title": "Digital Exodus at TechCorp",
    "description": "Competitor showing signs of major layoffs affecting 200+ employees",
    "companies_affected": ["techcorp.com"],
    "impact_score": 0.87,
    "recommended_actions": [
      "talent_poaching",
      "acquisition_evaluation",
      "market_positioning_shift"
    ],
    "data_sources": ["sixtyfour", "mixrank"],
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

### GET `/intelligence/signals`
Get active intelligence signals by type

**Response:**
```json
{
  "active_signals": {
    "competitor_distress": 3,
    "customer_churn_risk": 2,
    "financial_crisis": 1,
    "market_opportunity": 5,
    "security_threat": 0,
    "regulatory_change": 1
  },
  "signal_history": [
    {
      "type": "competitor_distress",
      "count": 3,
      "date": "2024-01-15"
    }
  ],
  "total_processed_today": 24,
  "autonomous_actions_triggered": 12
}
```

---

## Action Endpoints

### GET `/actions/recent`
Get recently executed actions for activity feed

**Response:**
```json
{
  "recent_actions": [
    {
      "id": "act_001",
      "action_type": "talent_poaching",
      "target": "competitor-xyz.com",
      "status": "completed",
      "business_impact": "$450K talent value acquired",
      "execution_time": "2.3s",
      "timestamp": "2024-01-15T10:30:00Z",
      "confidence": 0.87
    }
  ],
  "total_today": 24,
  "success_rate": 0.96
}
```

### GET `/actions/performance`
Get action performance analytics

**Response:**
```json
{
  "performance_by_category": {
    "financial": {
      "executed": 45,
      "success_rate": 0.94,
      "avg_roi": 125000
    },
    "competitive": {
      "executed": 38,
      "success_rate": 0.89, 
      "avg_roi": 200000
    }
  },
  "top_performing_actions": [
    {
      "action": "talent_poaching",
      "success_rate": 0.95,
      "avg_roi": 250000
    }
  ],
  "execution_trends": {
    "daily_average": 28,
    "weekly_trend": "+12%",
    "monthly_total": 756
  }
}
```

---

## Real-time Endpoints

### GET `/realtime/status`
Get real-time system status

**Response:**
```json
{
  "agent_status": "operational",
  "active_processes": 3,
  "queue_length": 2,
  "last_intelligence_update": "2024-01-15T10:28:00Z",
  "system_load": 0.45,
  "memory_usage": 0.62
}
```

---

## Frontend Integration Examples

### React/Next.js Dashboard Hook
```javascript
import { useState, useEffect } from 'react';

export const useDashboardData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await fetch('http://localhost:8001/dashboard/overview');
        const dashboardData = await response.json();
        setData(dashboardData);
      } catch (error) {
        console.error('Dashboard fetch failed:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
    const interval = setInterval(fetchDashboard, 30000); // Update every 30s
    return () => clearInterval(interval);
  }, []);

  return { data, loading };
};
```

### Company Research Component
```javascript
const CompanyResearch = () => {
  const [company, setCompany] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const researchCompany = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8001/research/company', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_domain: company,
          research_depth: 'standard',
          include_competitors: true
        })
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Research failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        value={company}
        onChange={(e) => setCompany(e.target.value)}
        placeholder="Enter company domain (e.g., anthropic.com)"
      />
      <button onClick={researchCompany} disabled={loading}>
        {loading ? 'Researching...' : 'Research Company'}
      </button>
      
      {results && (
        <div className="research-results">
          <h3>{results.company}</h3>
          <p>Financial Health: {results.financial_health}</p>
          <p>Employees: {results.employee_count}</p>
          <p>Tech Stack: {results.technology_stack.join(', ')}</p>
        </div>
      )}
    </div>
  );
};
```

### Agent Query Interface
```javascript
const AgentChat = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);

  const askAgent = async () => {
    const res = await fetch('http://localhost:8001/agent/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await res.json();
    setResponse(data);
  };

  return (
    <div className="agent-chat">
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask the autonomous agent anything..."
      />
      <button onClick={askAgent}>Ask Agent</button>
      
      {response && (
        <div className="agent-response">
          <p><strong>Agent:</strong> {response.response}</p>
          <div className="suggested-actions">
            <strong>Suggested Actions:</strong>
            {response.suggested_actions.map(action => (
              <span key={action} className="action-tag">{action}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
```

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error description",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (agent not initialized)

---

## Data Models

### CompanyIntelligenceResponse
Complete company intelligence data structure

### MarketInsightResponse  
Market insights with actionable recommendations

### DashboardDataResponse
Dashboard overview metrics and highlights

### AgentQueryRequest
Query structure for agent interaction

---

## Rate Limits

- **Dashboard endpoints:** 60 requests/minute
- **Research endpoints:** 20 requests/minute (due to external API calls)
- **Agent query:** 30 requests/minute
- **Real-time endpoints:** 120 requests/minute

---

## WebSocket Support (Future)

Real-time updates via WebSocket connection:
```javascript
const ws = new WebSocket('ws://localhost:8001/ws');
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  // Handle real-time intelligence updates
};
```

---

## Deployment

### Production Configuration
```python
# In frontend_api.py
uvicorn.run(
    "frontend_api:app",
    host="0.0.0.0",
    port=8001,
    workers=4,
    reload=False
)
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["python", "frontend_api.py"]
```

---

## Support

For API support and issues:
- Documentation: `/docs` endpoint
- Health Check: `/health` endpoint
- System Status: `/realtime/status` endpoint

The Pensieve Frontend API provides everything needed to build sophisticated business intelligence dashboards with real-time autonomous agent capabilities.