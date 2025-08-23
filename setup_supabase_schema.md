# 🚀 Quick Supabase Schema Setup

## Step 1: Copy the SQL Schema
1. Open `database/supabase_schema.sql` 
2. Copy the entire contents (Ctrl+A, Ctrl+C)

## Step 2: Run in Supabase Dashboard
1. Go to your Supabase project: https://gpqahficnzoavdcvkhyu.supabase.co
2. Click on the **SQL Editor** in the sidebar
3. Click **"New Query"**
4. Paste the entire schema SQL
5. Click **"Run"** (or press F5)

## Step 3: Verify Setup
The SQL will create:
- ✅ 11 tables (ai_decisions, business_events, performance_metrics, etc.)
- ✅ Indexes for performance
- ✅ Functions for analytics
- ✅ Views for common queries
- ✅ Row Level Security policies
- ✅ Sample data

## Step 4: Test Connection
Once the schema is set up, run:
```bash
python test_supabase.py
```

## What the Schema Creates

### Core Tables:
- `ai_decisions` - AI decision tracking
- `business_events` - Business event logging  
- `performance_metrics` - System performance data
- `financial_snapshots` - Financial intelligence data
- `customer_insights` - Customer intelligence data
- `market_insights` - Market intelligence data
- `technology_insights` - Technology intelligence data
- `system_status` - Component health monitoring
- `alert_history` - Alert audit trail
- `decision_outcomes` - Decision success tracking

### Helpful Views:
- `recent_high_confidence_decisions` - Recent confident AI decisions
- `system_health_overview` - Component health summary
- `critical_events_24h` - Critical events from last 24 hours
- `performance_trends` - Performance trending data

The setup takes about 30 seconds to complete in Supabase.