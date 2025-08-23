# Mock Financial Data Scenarios

The Pensieve CIO system now uses realistic mock financial data instead of requiring the Brex API. This provides full functionality for development, testing, and demonstrations.

## Available Company Profiles

### 1. Healthy SaaS (`healthy_saas`)
- **Stage**: Series A
- **Scenario**: Healthy Growth
- **Monthly Revenue**: $85,000
- **Employees**: 25
- **Funding Raised**: $8M
- **Runway**: 18 months target
- **Characteristics**: Steady growth, balanced burn rate, good cash management

### 2. Cash Crunch Startup (`cash_crunch_startup`)
- **Stage**: Seed
- **Scenario**: Cash Crunch
- **Monthly Revenue**: $15,000
- **Employees**: 8
- **Funding Raised**: $1.2M
- **Runway**: 6 months target
- **Characteristics**: Low runway, revenue struggles, cost-cutting mode

### 3. Post-Funding Scale (`post_funding_scale`)
- **Stage**: Series B
- **Scenario**: Post-Funding Growth
- **Monthly Revenue**: $250,000
- **Employees**: 75
- **Funding Raised**: $25M
- **Runway**: 24 months target
- **Characteristics**: High burn rate, aggressive scaling, strong revenue growth

### 4. Seasonal E-commerce (`seasonal_ecommerce`)
- **Stage**: Series A
- **Scenario**: Seasonal Business
- **Monthly Revenue**: $120,000 (highly variable)
- **Employees**: 35
- **Funding Raised**: $12M
- **Runway**: 15 months target
- **Characteristics**: Variable revenue, seasonal patterns, complex cash flow

## Financial Scenarios Available for Testing

### Critical Runway Scenario
```json
{
  "scenario": "critical_runway",
  "triggers": [
    "Runway below 30 days",
    "Immediate cash flow alerts",
    "Emergency funding recommendations"
  ],
  "ai_actions": [
    "Emergency expense freeze",
    "Funding deck preparation", 
    "Leadership alerts"
  ]
}
```

### Burn Rate Spike Scenario
```json
{
  "scenario": "burn_rate_spike", 
  "triggers": [
    "25%+ increase in monthly burn",
    "Large unexpected expenses",
    "Infrastructure scaling costs"
  ],
  "ai_actions": [
    "Burn rate analysis",
    "Expense optimization recommendations",
    "Scaling strategy review"
  ]
}
```

### Revenue Drop Scenario
```json
{
  "scenario": "revenue_drop",
  "triggers": [
    "40%+ revenue decline",
    "Customer churn spike",
    "Market downturn impact"
  ],
  "ai_actions": [
    "Customer retention campaigns",
    "Cost reduction strategies",
    "Revenue recovery planning"
  ]
}
```

### Large Expense Alert
```json
{
  "scenario": "large_expense",
  "triggers": [
    "Single expenses >$10k",
    "Unusual spending patterns",
    "Vendor payment spikes"
  ],
  "ai_actions": [
    "Expense approval workflows",
    "Budget impact analysis",
    "Vendor relationship review"
  ]
}
```

## Mock Data Features

### Realistic Transaction Data
- **90 days** of transaction history
- **Categorized expenses**: Software, Payroll, Marketing, Travel, Office
- **Revenue patterns** based on company stage and scenario
- **Seasonal variations** and market conditions
- **Large expense events** (monthly payroll, infrastructure costs)

### Dynamic Financial Metrics
- **Real-time cash flow** calculations
- **Burn rate trends** with scenario-specific patterns  
- **Runway predictions** based on current trajectory
- **Expense categorization** and analysis
- **Growth rate modeling** across different business stages

### Intelligent Alert Generation
The system automatically generates realistic financial alerts based on:
- Company stage and maturity
- Current financial scenario
- Historical spending patterns
- Industry benchmarks
- Seasonal factors

## Testing AI Decision Making

### Scenario Simulation Tool
Use the `simulate_financial_scenario` tool to trigger specific financial events:

```python
# Trigger critical runway scenario
await financial_monitor.simulate_financial_scenario({
    "scenario": "critical_runway",
    "profile": "cash_crunch_startup"  # Optional: change company profile
})

# Test AI response to burn rate spike
await financial_monitor.simulate_financial_scenario({
    "scenario": "burn_rate_spike"
})
```

### Expected AI Responses

#### Critical Runway (< 30 days)
- **Confidence**: 0.9+
- **Action**: `emergency_funding_prep`
- **Reasoning**: "Critical cash position requires immediate funding"
- **Timeline**: 2-4 weeks for funding round

#### Burn Rate Spike (25%+ increase)
- **Confidence**: 0.8+
- **Action**: `expense_optimization`
- **Reasoning**: "Unsustainable burn rate increase detected"
- **Target**: 15-25% cost reduction

#### Revenue Drop (40%+ decline)
- **Confidence**: 0.85+
- **Action**: `launch_retention_campaign`
- **Reasoning**: "Revenue decline threatens business sustainability"
- **Focus**: Customer retention and churn prevention

## Configuration

### Environment Variables
```env
USE_MOCK_DATA=true
DEMO_FINANCIAL_PROFILE=healthy_saas
CRITICAL_CASH_RUNWAY_DAYS=30
```

### Available Profiles
- `healthy_saas` (default)
- `cash_crunch_startup` 
- `post_funding_scale`
- `seasonal_ecommerce`

### Dynamic Profile Switching
The system supports switching financial profiles at runtime through the simulation tool, allowing testing of different business scenarios without restart.

## Integration with AI Decision Engine

The mock financial data integrates seamlessly with the Gemini-powered decision engine:

1. **Real-time Monitoring**: Continuous analysis of mock financial metrics
2. **Pattern Detection**: Identification of concerning trends and opportunities
3. **Contextual Decisions**: AI considers company stage, scenario, and historical patterns
4. **Action Execution**: Automated responses based on confidence thresholds
5. **Learning Loop**: Decision outcomes inform future pattern recognition

This comprehensive mock system enables full testing and development of the autonomous AI CIO without requiring real financial API access.