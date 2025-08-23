-- Pensieve CIO Supabase Database Schema
-- Run this SQL in your Supabase SQL editor to create the required tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- AI Decisions Table
CREATE TABLE ai_decisions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    decision_type VARCHAR(100) NOT NULL,
    confidence DECIMAL(3,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    reasoning TEXT NOT NULL,
    action_taken JSONB NOT NULL,
    context JSONB NOT NULL,
    outcome VARCHAR(50),
    component VARCHAR(100) DEFAULT 'decision_orchestrator',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX idx_ai_decisions_type ON ai_decisions(decision_type);
CREATE INDEX idx_ai_decisions_confidence ON ai_decisions(confidence);
CREATE INDEX idx_ai_decisions_created_at ON ai_decisions(created_at);
CREATE INDEX idx_ai_decisions_component ON ai_decisions(component);

-- Business Events Table
CREATE TABLE business_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    component VARCHAR(100) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_business_events_type ON business_events(event_type);
CREATE INDEX idx_business_events_priority ON business_events(priority);
CREATE INDEX idx_business_events_component ON business_events(component);
CREATE INDEX idx_business_events_created_at ON business_events(created_at);

-- Performance Metrics Table
CREATE TABLE performance_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    value DECIMAL(15,4) NOT NULL,
    unit VARCHAR(20),
    component VARCHAR(100) NOT NULL,
    tags JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_performance_metrics_name ON performance_metrics(metric_name);
CREATE INDEX idx_performance_metrics_component ON performance_metrics(component);
CREATE INDEX idx_performance_metrics_timestamp ON performance_metrics(timestamp);

-- Financial Snapshots Table
CREATE TABLE financial_snapshots (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    company_profile VARCHAR(100) NOT NULL,
    cash_flow_data JSONB NOT NULL,
    scenario VARCHAR(50),
    metadata JSONB DEFAULT '{}',
    captured_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_financial_snapshots_profile ON financial_snapshots(company_profile);
CREATE INDEX idx_financial_snapshots_scenario ON financial_snapshots(scenario);
CREATE INDEX idx_financial_snapshots_captured_at ON financial_snapshots(captured_at);

-- Customer Insights Table
CREATE TABLE customer_insights (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    insight_type VARCHAR(100) NOT NULL,
    customer_data JSONB NOT NULL,
    risk_score DECIMAL(3,2) CHECK (risk_score >= 0 AND risk_score <= 1),
    action_taken VARCHAR(100),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_customer_insights_type ON customer_insights(insight_type);
CREATE INDEX idx_customer_insights_risk_score ON customer_insights(risk_score);
CREATE INDEX idx_customer_insights_created_at ON customer_insights(created_at);

-- Market Insights Table
CREATE TABLE market_insights (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    insight_type VARCHAR(100) NOT NULL,
    market_data JSONB NOT NULL,
    opportunity_score DECIMAL(3,2) CHECK (opportunity_score >= 0 AND opportunity_score <= 1),
    threat_score DECIMAL(3,2) CHECK (threat_score >= 0 AND threat_score <= 1),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_market_insights_type ON market_insights(insight_type);
CREATE INDEX idx_market_insights_opportunity ON market_insights(opportunity_score);
CREATE INDEX idx_market_insights_threat ON market_insights(threat_score);
CREATE INDEX idx_market_insights_created_at ON market_insights(created_at);

-- Technology Insights Table
CREATE TABLE technology_insights (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    insight_type VARCHAR(100) NOT NULL,
    tech_data JSONB NOT NULL,
    impact_score DECIMAL(3,2) CHECK (impact_score >= 0 AND impact_score <= 1),
    adoption_trend VARCHAR(50),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_technology_insights_type ON technology_insights(insight_type);
CREATE INDEX idx_technology_insights_impact ON technology_insights(impact_score);
CREATE INDEX idx_technology_insights_trend ON technology_insights(adoption_trend);
CREATE INDEX idx_technology_insights_created_at ON technology_insights(created_at);

-- System Status Table
CREATE TABLE system_status (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    component VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('healthy', 'warning', 'error', 'maintenance')),
    health_score DECIMAL(3,2) CHECK (health_score >= 0 AND health_score <= 1),
    last_error TEXT,
    metadata JSONB DEFAULT '{}',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_system_status_component ON system_status(component);
CREATE INDEX idx_system_status_status ON system_status(status);
CREATE INDEX idx_system_status_updated_at ON system_status(updated_at);

-- Alert History Table (for tracking all system alerts)
CREATE TABLE alert_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    source_component VARCHAR(100) NOT NULL,
    alert_data JSONB NOT NULL,
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_action TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_alert_history_type ON alert_history(alert_type);
CREATE INDEX idx_alert_history_severity ON alert_history(severity);
CREATE INDEX idx_alert_history_source ON alert_history(source_component);
CREATE INDEX idx_alert_history_resolved ON alert_history(resolved);
CREATE INDEX idx_alert_history_created_at ON alert_history(created_at);

-- Decision Outcomes Table (for tracking decision success/failure)
CREATE TABLE decision_outcomes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    decision_id UUID REFERENCES ai_decisions(id) ON DELETE CASCADE,
    outcome_type VARCHAR(50) NOT NULL CHECK (outcome_type IN ('success', 'failure', 'partial', 'pending')),
    impact_metrics JSONB DEFAULT '{}',
    feedback_score DECIMAL(3,2) CHECK (feedback_score >= 0 AND feedback_score <= 1),
    notes TEXT,
    measured_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_decision_outcomes_decision_id ON decision_outcomes(decision_id);
CREATE INDEX idx_decision_outcomes_type ON decision_outcomes(outcome_type);
CREATE INDEX idx_decision_outcomes_measured_at ON decision_outcomes(measured_at);

-- Create Views for Common Queries

-- Recent High-Confidence Decisions View
CREATE VIEW recent_high_confidence_decisions AS
SELECT 
    decision_type,
    confidence,
    reasoning,
    action_taken,
    created_at,
    CASE 
        WHEN outcome IS NOT NULL THEN outcome
        ELSE 'pending'
    END as status
FROM ai_decisions 
WHERE confidence > 0.8 
    AND created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;

-- System Health Overview
CREATE VIEW system_health_overview AS
SELECT 
    component,
    status,
    health_score,
    CASE 
        WHEN updated_at < NOW() - INTERVAL '1 hour' THEN 'stale'
        ELSE 'current'
    END as data_freshness,
    updated_at
FROM system_status
ORDER BY 
    CASE status 
        WHEN 'error' THEN 1
        WHEN 'warning' THEN 2
        WHEN 'maintenance' THEN 3
        WHEN 'healthy' THEN 4
    END,
    component;

-- Critical Events in Last 24 Hours
CREATE VIEW critical_events_24h AS
SELECT 
    event_type,
    component,
    event_data,
    created_at
FROM business_events 
WHERE priority = 'critical' 
    AND created_at >= NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;

-- Performance Trends View
CREATE VIEW performance_trends AS
SELECT 
    metric_name,
    component,
    AVG(value) as avg_value,
    MIN(value) as min_value,
    MAX(value) as max_value,
    COUNT(*) as data_points,
    DATE_TRUNC('hour', timestamp) as hour_bucket
FROM performance_metrics
WHERE timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY metric_name, component, DATE_TRUNC('hour', timestamp)
ORDER BY hour_bucket DESC, metric_name, component;

-- Create RLS (Row Level Security) Policies
-- Enable RLS on all tables
ALTER TABLE ai_decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE business_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE customer_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE market_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE technology_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_status ENABLE ROW LEVEL SECURITY;
ALTER TABLE alert_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE decision_outcomes ENABLE ROW LEVEL SECURITY;

-- Create policies that allow service key full access
-- (In production, you'd want more granular policies based on user roles)

-- Service role policies (full access)
CREATE POLICY "Service role can do everything on ai_decisions" ON ai_decisions
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on business_events" ON business_events
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on performance_metrics" ON performance_metrics
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on financial_snapshots" ON financial_snapshots
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on customer_insights" ON customer_insights
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on market_insights" ON market_insights
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on technology_insights" ON technology_insights
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on system_status" ON system_status
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on alert_history" ON alert_history
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role can do everything on decision_outcomes" ON decision_outcomes
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- Anon role policies (read-only for public data)
CREATE POLICY "Anon can read system health" ON system_status
    FOR SELECT USING (true);

CREATE POLICY "Anon can read public business events" ON business_events
    FOR SELECT USING (metadata->>'public' = 'true');

-- Create Functions for Common Operations

-- Function to get decision success rate
CREATE OR REPLACE FUNCTION get_decision_success_rate(
    decision_type_param TEXT DEFAULT NULL,
    days_back INTEGER DEFAULT 7
)
RETURNS TABLE(
    decision_type TEXT,
    total_decisions BIGINT,
    successful_decisions BIGINT,
    success_rate DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.decision_type::TEXT,
        COUNT(d.id) as total_decisions,
        COUNT(outcomes.id) FILTER (WHERE outcomes.outcome_type = 'success') as successful_decisions,
        CASE 
            WHEN COUNT(d.id) > 0 THEN 
                ROUND(COUNT(outcomes.id) FILTER (WHERE outcomes.outcome_type = 'success')::DECIMAL / COUNT(d.id) * 100, 2)
            ELSE 0
        END as success_rate
    FROM ai_decisions d
    LEFT JOIN decision_outcomes outcomes ON d.id = outcomes.decision_id
    WHERE d.created_at >= NOW() - (days_back || ' days')::INTERVAL
        AND (decision_type_param IS NULL OR d.decision_type = decision_type_param)
    GROUP BY d.decision_type
    ORDER BY success_rate DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to cleanup old data
CREATE OR REPLACE FUNCTION cleanup_old_data(days_to_keep INTEGER DEFAULT 90)
RETURNS TABLE(
    table_name TEXT,
    records_deleted BIGINT
) AS $$
DECLARE
    cutoff_date TIMESTAMP WITH TIME ZONE;
BEGIN
    cutoff_date := NOW() - (days_to_keep || ' days')::INTERVAL;
    
    -- Clean up performance metrics
    WITH deleted AS (
        DELETE FROM performance_metrics 
        WHERE timestamp < cutoff_date 
        RETURNING *
    )
    SELECT 'performance_metrics'::TEXT, COUNT(*)::BIGINT FROM deleted;
    
    -- Clean up business events (keep critical events longer)
    WITH deleted AS (
        DELETE FROM business_events 
        WHERE created_at < cutoff_date AND priority != 'critical'
        RETURNING *
    )
    SELECT 'business_events'::TEXT, COUNT(*)::BIGINT FROM deleted;
    
    -- Clean up financial snapshots
    WITH deleted AS (
        DELETE FROM financial_snapshots 
        WHERE captured_at < cutoff_date 
        RETURNING *
    )
    SELECT 'financial_snapshots'::TEXT, COUNT(*)::BIGINT FROM deleted;
    
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Create Triggers for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add trigger to ai_decisions
CREATE TRIGGER update_ai_decisions_updated_at 
    BEFORE UPDATE ON ai_decisions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add trigger to system_status
CREATE TRIGGER update_system_status_updated_at 
    BEFORE UPDATE ON system_status 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert initial system status for all components
INSERT INTO system_status (component, status, health_score) VALUES
    ('decision_orchestrator', 'healthy', 1.0),
    ('event_processor', 'healthy', 1.0),
    ('brex_financial_monitor', 'healthy', 1.0),
    ('pylon_customer_intelligence', 'healthy', 1.0),
    ('sixtyfour_market_intelligence', 'healthy', 1.0),
    ('mixrank_technology_intelligence', 'healthy', 1.0),
    ('pensieve_cio', 'healthy', 1.0)
ON CONFLICT (component) DO NOTHING;

-- Create Health Check Table (for connection testing)
CREATE TABLE _health_check (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    status TEXT DEFAULT 'ok',
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert a health check record
INSERT INTO _health_check (status) VALUES ('ok');

-- Grant permissions (adjust based on your security needs)
-- These grants are for the service role - adjust as needed
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;