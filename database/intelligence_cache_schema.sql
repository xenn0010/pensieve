-- Intelligence Cache Schema for SixtyFour Data
-- Stores pre-fetched company intelligence for instant Gemini access

-- Table for cached company intelligence
CREATE TABLE IF NOT EXISTS intelligence_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    company_domain TEXT,
    research_depth TEXT NOT NULL DEFAULT 'basic', -- basic, standard, maximum
    intelligence_type TEXT NOT NULL DEFAULT 'competitive', -- competitive, financial, strategic
    
    -- Cached data fields
    financial_health JSONB,
    competitive_signals JSONB,
    strategic_shifts JSONB,
    customer_intelligence JSONB,
    market_opportunities JSONB,
    insider_threats JSONB,
    regulatory_risks JSONB,
    
    -- Raw response for debugging
    raw_response JSONB,
    
    -- Cache metadata
    cached_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 0,
    
    -- Job tracking
    sixtyfour_job_id TEXT,
    cache_status TEXT NOT NULL DEFAULT 'pending', -- pending, processing, completed, failed, expired
    error_message TEXT,
    
    -- Performance metrics
    fetch_duration_seconds REAL,
    data_size_bytes INTEGER,
    
    UNIQUE(company_name, research_depth, intelligence_type)
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_intelligence_cache_lookup 
ON intelligence_cache(company_name, research_depth, intelligence_type);

CREATE INDEX IF NOT EXISTS idx_intelligence_cache_status 
ON intelligence_cache(cache_status);

CREATE INDEX IF NOT EXISTS idx_intelligence_cache_expires 
ON intelligence_cache(expires_at);

-- Table for tracking pre-fetch priorities
CREATE TABLE IF NOT EXISTS intelligence_prefetch_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    company_domain TEXT,
    research_depth TEXT NOT NULL DEFAULT 'standard',
    intelligence_type TEXT NOT NULL DEFAULT 'competitive',
    
    priority INTEGER NOT NULL DEFAULT 50, -- 1-100, higher = more important
    requested_by TEXT, -- component that requested this
    requested_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    status TEXT NOT NULL DEFAULT 'queued', -- queued, processing, completed, failed
    processing_started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Scheduling
    schedule_after TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    
    UNIQUE(company_name, research_depth, intelligence_type)
);

-- Index for queue processing
CREATE INDEX IF NOT EXISTS idx_prefetch_queue_processing 
ON intelligence_prefetch_queue(status, priority DESC, schedule_after);

-- Table for intelligence access patterns (for ML optimization)
CREATE TABLE IF NOT EXISTS intelligence_access_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    intelligence_type TEXT NOT NULL,
    accessed_by TEXT NOT NULL, -- component or user
    accessed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Context about the access
    trigger_event TEXT, -- what caused this lookup
    decision_context JSONB, -- what decision was being made
    cache_hit BOOLEAN NOT NULL DEFAULT true,
    
    -- Performance
    response_time_ms INTEGER
);

-- View for cache analytics
CREATE OR REPLACE VIEW intelligence_cache_analytics AS
SELECT 
    company_name,
    intelligence_type,
    research_depth,
    cache_status,
    AGE(NOW(), cached_at) as cache_age,
    access_count,
    CASE 
        WHEN expires_at < NOW() THEN 'expired'
        WHEN cache_status = 'completed' THEN 'fresh'
        ELSE cache_status
    END as effective_status,
    fetch_duration_seconds,
    data_size_bytes
FROM intelligence_cache
ORDER BY last_accessed_at DESC;

-- Function to get fresh intelligence (with cache fallback)
CREATE OR REPLACE FUNCTION get_company_intelligence(
    p_company_name TEXT,
    p_research_depth TEXT DEFAULT 'standard',
    p_intelligence_type TEXT DEFAULT 'competitive'
) 
RETURNS JSONB AS $$
DECLARE
    cache_record RECORD;
    result JSONB;
BEGIN
    -- Try to get from cache first
    SELECT * INTO cache_record
    FROM intelligence_cache 
    WHERE company_name = p_company_name 
      AND research_depth = p_research_depth
      AND intelligence_type = p_intelligence_type
      AND cache_status = 'completed'
      AND expires_at > NOW()
    ORDER BY cached_at DESC
    LIMIT 1;
    
    IF FOUND THEN
        -- Update access tracking
        UPDATE intelligence_cache 
        SET 
            last_accessed_at = NOW(),
            access_count = access_count + 1
        WHERE id = cache_record.id;
        
        -- Build result from cached fields
        result := jsonb_build_object(
            'financial_health', cache_record.financial_health,
            'competitive_signals', cache_record.competitive_signals,
            'strategic_shifts', cache_record.strategic_shifts,
            'customer_intelligence', cache_record.customer_intelligence,
            'market_opportunities', cache_record.market_opportunities,
            'insider_threats', cache_record.insider_threats,
            'regulatory_risks', cache_record.regulatory_risks,
            'cached_at', cache_record.cached_at,
            'cache_hit', true
        );
        
        RETURN result;
    ELSE
        -- No cache hit - queue for prefetch and return null
        INSERT INTO intelligence_prefetch_queue (
            company_name, research_depth, intelligence_type, 
            priority, requested_by
        ) VALUES (
            p_company_name, p_research_depth, p_intelligence_type,
            75, 'on_demand_request'
        ) ON CONFLICT (company_name, research_depth, intelligence_type) 
        DO UPDATE SET 
            priority = GREATEST(intelligence_prefetch_queue.priority, 75),
            requested_at = NOW();
            
        RETURN jsonb_build_object('cache_hit', false, 'queued_for_fetch', true);
    END IF;
END;
$$ LANGUAGE plpgsql;
