-- Enhanced Data Storage Schema for Pensieve
-- Stores ALL API results, search data, and research findings

-- Table for storing ALL API call results (not just cached intelligence)
CREATE TABLE IF NOT EXISTS api_call_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- API call metadata
    api_provider TEXT NOT NULL, -- 'sixtyfour', 'mixrank', 'brex', 'pylon'
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL DEFAULT 'GET',
    
    -- Request details
    request_params JSONB NOT NULL,
    request_headers JSONB,
    
    -- Response details  
    response_status INTEGER NOT NULL,
    response_headers JSONB,
    response_body JSONB, -- Full raw response
    response_size_bytes INTEGER,
    
    -- Timing and performance
    request_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    response_timestamp TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    
    -- Context and tracking
    triggered_by TEXT, -- 'user_search', 'autonomous_agent', 'scheduled_refresh'
    session_id TEXT,
    user_id TEXT,
    
    -- Processing status
    processing_status TEXT DEFAULT 'raw', -- 'raw', 'processed', 'stored', 'failed'
    error_message TEXT,
    
    -- Extracted entities (for search and analysis)
    extracted_companies TEXT[],
    extracted_people TEXT[],
    extracted_technologies TEXT[],
    extracted_metrics JSONB,
    
    UNIQUE(api_provider, endpoint, request_params, request_timestamp)
);

-- Table for storing processed search results
CREATE TABLE IF NOT EXISTS search_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Search metadata
    search_query TEXT NOT NULL,
    search_type TEXT NOT NULL, -- 'company', 'person', 'technology', 'market', 'financial'
    search_scope TEXT, -- 'basic', 'comprehensive', 'deep'
    
    -- Results data
    total_results INTEGER DEFAULT 0,
    results_data JSONB NOT NULL, -- Structured search results
    confidence_score REAL,
    
    -- Source tracking
    data_sources TEXT[], -- ['sixtyfour', 'mixrank', 'internal_cache']
    api_call_ids UUID[], -- References to api_call_results
    
    -- Performance and quality metrics
    search_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    processing_duration_ms INTEGER,
    data_freshness_hours REAL,
    quality_score REAL,
    
    -- User and session tracking
    requested_by TEXT,
    session_id TEXT,
    
    -- Result categorization
    result_categories TEXT[], -- ['financial_health', 'competitive_intel', 'market_trends']
    tags TEXT[],
    
    -- Storage and access tracking
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Table for storing research sessions (user or autonomous research workflows)
CREATE TABLE IF NOT EXISTS research_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Session metadata
    session_name TEXT,
    research_objective TEXT NOT NULL,
    research_type TEXT NOT NULL, -- 'competitive_analysis', 'market_research', 'due_diligence'
    
    -- Scope and targets
    target_companies TEXT[],
    target_people TEXT[],
    target_markets TEXT[],
    research_questions TEXT[],
    
    -- Session tracking
    started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'active', -- 'active', 'completed', 'paused', 'failed'
    
    -- Results and findings
    key_findings JSONB,
    data_summary JSONB,
    confidence_assessment JSONB,
    
    -- Related data
    search_result_ids UUID[], -- References to search_results
    api_call_ids UUID[], -- References to api_call_results
    intelligence_cache_ids UUID[], -- References to intelligence_cache
    
    -- User and automation tracking
    initiated_by TEXT NOT NULL, -- 'user:email', 'autonomous_agent:name'
    automation_level TEXT DEFAULT 'manual', -- 'manual', 'assisted', 'autonomous'
    
    -- Performance metrics
    total_api_calls INTEGER DEFAULT 0,
    total_cost_estimate REAL,
    data_sources_used TEXT[],
    
    -- Output and sharing
    report_generated BOOLEAN DEFAULT FALSE,
    report_url TEXT,
    shared_with TEXT[]
);

-- Table for storing company profiles (aggregated from all sources)
CREATE TABLE IF NOT EXISTS company_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Company identification
    company_name TEXT NOT NULL,
    company_domain TEXT,
    company_aliases TEXT[], -- Alternative names, abbreviations
    
    -- Basic information
    industry TEXT,
    size_category TEXT, -- 'startup', 'scaleup', 'enterprise'
    headquarters_location TEXT,
    founded_year INTEGER,
    
    -- Current data snapshot (aggregated from all sources)
    financial_metrics JSONB,
    employee_metrics JSONB,
    technology_stack JSONB,
    competitive_position JSONB,
    market_presence JSONB,
    risk_indicators JSONB,
    
    -- Data provenance and quality
    data_sources TEXT[] NOT NULL,
    last_updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    data_quality_score REAL,
    data_completeness_percent REAL,
    
    -- Related records
    related_search_results UUID[],
    related_api_calls UUID[],
    related_research_sessions UUID[],
    
    -- Monitoring and tracking
    monitoring_enabled BOOLEAN DEFAULT FALSE,
    alert_thresholds JSONB,
    last_monitored_at TIMESTAMP WITH TIME ZONE,
    
    -- Access and usage
    times_researched INTEGER DEFAULT 0,
    last_researched_at TIMESTAMP WITH TIME ZONE,
    research_priority INTEGER DEFAULT 50, -- 1-100
    
    UNIQUE(company_name, company_domain)
);

-- Table for storing extracted insights and intelligence findings
CREATE TABLE IF NOT EXISTS intelligence_findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Finding metadata
    finding_type TEXT NOT NULL, -- 'financial_trend', 'competitive_threat', 'market_opportunity'
    confidence_level TEXT NOT NULL, -- 'high', 'medium', 'low'
    
    -- Finding details
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    key_metrics JSONB,
    supporting_evidence JSONB,
    
    -- Context and relationships
    related_companies TEXT[],
    related_people TEXT[],
    impact_assessment TEXT,
    urgency_level TEXT, -- 'immediate', 'high', 'medium', 'low'
    
    -- Data sources and validation
    source_api_calls UUID[],
    source_search_results UUID[],
    validation_status TEXT DEFAULT 'unvalidated', -- 'unvalidated', 'validated', 'disputed'
    
    -- Discovery and processing
    discovered_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    discovered_by TEXT NOT NULL, -- AI agent or user
    processing_method TEXT, -- 'pattern_detection', 'anomaly_analysis', 'manual_review'
    
    -- Action and follow-up
    action_required BOOLEAN DEFAULT FALSE,
    action_taken TEXT,
    follow_up_needed BOOLEAN DEFAULT FALSE,
    
    -- Monitoring and lifecycle
    expires_at TIMESTAMP WITH TIME ZONE,
    archived BOOLEAN DEFAULT FALSE,
    archived_reason TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_api_call_results_provider_timestamp 
ON api_call_results(api_provider, request_timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_api_call_results_status 
ON api_call_results(response_status, processing_status);

CREATE INDEX IF NOT EXISTS idx_search_results_query 
ON search_results USING gin(to_tsvector('english', search_query));

CREATE INDEX IF NOT EXISTS idx_search_results_type_timestamp 
ON search_results(search_type, search_timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_research_sessions_status 
ON research_sessions(status, started_at DESC);

CREATE INDEX IF NOT EXISTS idx_company_profiles_name 
ON company_profiles USING gin(to_tsvector('english', company_name));

CREATE INDEX IF NOT EXISTS idx_company_profiles_domain 
ON company_profiles(company_domain);

CREATE INDEX IF NOT EXISTS idx_intelligence_findings_type 
ON intelligence_findings(finding_type, confidence_level, discovered_at DESC);

-- Views for common queries
CREATE OR REPLACE VIEW recent_api_activity AS
SELECT 
    api_provider,
    endpoint,
    COUNT(*) as call_count,
    AVG(duration_ms) as avg_duration_ms,
    COUNT(CASE WHEN response_status >= 200 AND response_status < 300 THEN 1 END) as success_count,
    MAX(request_timestamp) as last_call_at
FROM api_call_results 
WHERE request_timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY api_provider, endpoint
ORDER BY call_count DESC;

CREATE OR REPLACE VIEW company_research_summary AS
SELECT 
    cp.company_name,
    cp.company_domain,
    cp.industry,
    cp.data_quality_score,
    cp.times_researched,
    cp.last_researched_at,
    COUNT(DISTINCT sr.id) as search_results_count,
    COUNT(DISTINCT rs.id) as research_sessions_count,
    COUNT(DISTINCT if_findings.id) as intelligence_findings_count
FROM company_profiles cp
LEFT JOIN search_results sr ON cp.company_name = ANY(string_to_array(sr.search_query, ' '))
LEFT JOIN research_sessions rs ON cp.company_name = ANY(rs.target_companies)
LEFT JOIN intelligence_findings if_findings ON cp.company_name = ANY(if_findings.related_companies)
GROUP BY cp.id, cp.company_name, cp.company_domain, cp.industry, cp.data_quality_score, cp.times_researched, cp.last_researched_at
ORDER BY cp.times_researched DESC, cp.last_researched_at DESC;

-- Functions for data management
CREATE OR REPLACE FUNCTION store_api_call_result(
    p_api_provider TEXT,
    p_endpoint TEXT,
    p_method TEXT,
    p_request_params JSONB,
    p_response_status INTEGER,
    p_response_body JSONB,
    p_duration_ms INTEGER DEFAULT NULL,
    p_triggered_by TEXT DEFAULT NULL
) RETURNS UUID AS $$
DECLARE
    result_id UUID;
BEGIN
    INSERT INTO api_call_results (
        api_provider, endpoint, method, request_params,
        response_status, response_body, duration_ms, triggered_by,
        response_timestamp, processing_status
    ) VALUES (
        p_api_provider, p_endpoint, p_method, p_request_params,
        p_response_status, p_response_body, p_duration_ms, p_triggered_by,
        NOW(), 'raw'
    ) RETURNING id INTO result_id;
    
    RETURN result_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_company_research_data(
    p_company_name TEXT
) RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT json_build_object(
        'profile', (SELECT row_to_json(cp) FROM company_profiles cp WHERE cp.company_name ILIKE p_company_name),
        'recent_searches', (SELECT json_agg(sr) FROM search_results sr WHERE sr.search_query ILIKE '%' || p_company_name || '%' ORDER BY sr.search_timestamp DESC LIMIT 10),
        'research_sessions', (SELECT json_agg(rs) FROM research_sessions rs WHERE p_company_name = ANY(rs.target_companies) ORDER BY rs.started_at DESC LIMIT 5),
        'intelligence_findings', (SELECT json_agg(if_findings) FROM intelligence_findings if_findings WHERE p_company_name = ANY(if_findings.related_companies) ORDER BY if_findings.discovered_at DESC LIMIT 10),
        'cached_intelligence', (SELECT json_agg(ic) FROM intelligence_cache ic WHERE ic.company_name ILIKE p_company_name ORDER BY ic.cached_at DESC LIMIT 5)
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;
