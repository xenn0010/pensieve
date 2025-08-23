# Supabase Setup Guide for Pensieve CIO

This guide walks you through setting up Supabase as the database backend for your Pensieve CIO autonomous intelligence system.

## 🚀 Quick Setup

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create a new account
2. Create a new project
3. Choose a strong database password
4. Wait for project initialization (2-3 minutes)

### 2. Get Your Credentials
From your Supabase dashboard:
- **Project URL**: `https://your-project-id.supabase.co`
- **Anon Key**: Found in Settings > API
- **Service Role Key**: Found in Settings > API (keep this secret!)

### 3. Setup Database Schema
1. Go to SQL Editor in your Supabase dashboard
2. Copy the entire contents of `database/supabase_schema.sql`
3. Paste and run the SQL to create all tables and functions

### 4. Configure Environment Variables
Update your `.env` file:
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_key_here
```

## 📊 Database Schema Overview

### Core Intelligence Tables

#### `ai_decisions`
Stores all AI decision-making events with full context and outcomes.
```sql
- decision_type: Type of decision made
- confidence: AI confidence score (0-1)
- reasoning: Detailed explanation of decision
- action_taken: Parameters and actions executed
- context: Event context and business data
- outcome: Success/failure tracking
```

#### `business_events`
Logs all significant business events across the system.
```sql
- event_type: Category of business event
- event_data: Detailed event information
- priority: low/medium/high/critical
- component: Source system component
- metadata: Additional contextual data
```

#### `performance_metrics`
Tracks system performance and operational metrics.
```sql
- metric_name: Name of the performance metric
- value: Numerical metric value
- unit: Measurement unit
- component: Component that generated metric
- tags: Key-value metadata tags
```

### Intelligence Storage Tables

#### `financial_snapshots`
Stores financial intelligence data and analysis.
```sql
- company_profile: Business profile identifier
- cash_flow_data: Complete financial analysis
- scenario: Current financial scenario
- metadata: Additional business context
```

#### `customer_insights`
Customer intelligence and churn analysis data.
```sql
- insight_type: Type of customer insight
- customer_data: Customer analysis results
- risk_score: Churn/risk probability (0-1)
- action_taken: Automated actions performed
```

#### `market_insights`
Market intelligence and competitive analysis.
```sql
- insight_type: Market analysis category
- market_data: Market intelligence results
- opportunity_score: Market opportunity rating
- threat_score: Competitive threat rating
```

#### `technology_insights`
Technology stack and adoption intelligence.
```sql
- insight_type: Technology analysis type
- tech_data: Technology intelligence results
- impact_score: Technology impact rating
- adoption_trend: Technology adoption direction
```

### System Management Tables

#### `system_status`
Real-time health monitoring for all components.
```sql
- component: System component identifier
- status: healthy/warning/error/maintenance
- health_score: Overall health rating (0-1)
- last_error: Most recent error message
- metadata: Component-specific status data
```

#### `alert_history`
Complete audit trail of all system alerts.
```sql
- alert_type: Category of alert
- severity: Alert severity level
- source_component: Component that generated alert
- alert_data: Complete alert information
- resolved: Whether alert has been resolved
```

## 🔧 Advanced Configuration

### Row Level Security (RLS)
The schema includes RLS policies that:
- Grant full access to service role
- Provide read-only access to public data for anon users
- Secure sensitive intelligence data

### Database Functions
Pre-built functions for common operations:
- `get_decision_success_rate()`: Calculate AI decision success rates
- `cleanup_old_data()`: Automatic data retention management

### Performance Optimization
- Comprehensive indexing on all query patterns
- Automatic timestamp triggers
- Efficient JSONB storage for complex data
- Time-based partitioning for high-volume tables

## 📈 API Endpoints

With Supabase integrated, Pensieve CIO provides rich API endpoints:

### `/metrics`
```json
{
  "decision_analytics": {
    "total_decisions": 45,
    "avg_confidence": 0.82,
    "high_confidence_decisions": 38,
    "success_rate": 0.89
  },
  "system_components": [...],
  "database_connected": true
}
```

### `/decisions?limit=50`
```json
{
  "decisions": [
    {
      "decision_type": "optimize_cash_flow",
      "confidence": 0.89,
      "reasoning": "Critical runway detected...",
      "action_taken": {...},
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 45
}
```

### `/events?priority=critical`
```json
{
  "events": [
    {
      "event_type": "financial_alert",
      "priority": "critical",
      "component": "brex_financial_monitor",
      "event_data": {...},
      "created_at": "2024-01-15T10:25:00Z"
    }
  ],
  "count": 3
}
```

### `/system-status`
```json
{
  "components": [
    {
      "component": "decision_orchestrator",
      "status": "healthy",
      "health_score": 0.98,
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "overall_health": "healthy"
}
```

## 🔒 Security Best Practices

### Environment Variables
- **Never commit** your service role key to version control
- **Use different keys** for development and production
- **Rotate keys regularly** in production environments

### Database Security
- RLS policies protect sensitive data
- Service role has full access for system operations
- Anon role has limited read access for public endpoints

### Network Security
- Configure Supabase network restrictions if needed
- Use HTTPS for all API communications
- Consider VPN access for sensitive operations

## 📊 Monitoring & Observability

### Built-in Analytics
- Real-time decision success rates
- Component health monitoring
- Performance metric trending
- Alert history and resolution tracking

### Custom Queries
Access Supabase SQL Editor to run custom analytics:
```sql
-- Get decision success rate by type
SELECT * FROM get_decision_success_rate('optimize_cash_flow', 7);

-- View recent critical events
SELECT * FROM critical_events_24h;

-- Check system health overview
SELECT * FROM system_health_overview;
```

### Data Retention
- Automatic cleanup of old performance metrics
- Configurable retention periods
- Critical events preserved longer
- AI decisions kept for learning and audit

## 🚀 Production Deployment

### Scaling Considerations
- Supabase handles automatic scaling
- Connection pooling included
- Read replicas available for high-traffic scenarios
- Built-in CDN for global performance

### Backup & Recovery
- Automatic daily backups included
- Point-in-time recovery available
- Export capabilities for data migration
- Disaster recovery procedures documented

### Cost Optimization
- Free tier supports development and light production use
- Pay-per-use scaling for growing businesses
- Monitor usage in Supabase dashboard
- Set up billing alerts for cost control

## 🔧 Development Tips

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your Supabase credentials

# Run the application
python main.py
```

### Testing Database Connection
```python
from config.supabase_client import supabase_client
import asyncio

async def test_connection():
    await supabase_client.initialize()
    print("✓ Supabase connected successfully!")

asyncio.run(test_connection())
```

### Debug Mode
Enable debug logging to see all database operations:
```env
DEBUG=true
```

This comprehensive Supabase integration provides enterprise-grade data management for your autonomous AI CIO system with real-time analytics, robust security, and scalable architecture.