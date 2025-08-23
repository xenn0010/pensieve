"""
Proposed API Extensions for Frontend Integration
This shows what endpoints we should add to main.py for comprehensive frontend support
"""

from fastapi import HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel

# Data Models for API Responses
class CompanyIntelligence(BaseModel):
    company: str
    financial_health: Optional[dict] = None
    competitive_signals: Optional[dict] = None
    strategic_shifts: Optional[dict] = None
    cache_hit: bool
    cached_at: Optional[str] = None

class ActionRequest(BaseModel):
    action_type: str
    parameters: dict
    manual_trigger: bool = True

class DashboardData(BaseModel):
    intelligence_cache_stats: dict
    recent_decisions: List[dict]
    system_health: dict
    active_jobs: List[dict]

# PROPOSED ENDPOINTS TO ADD TO main.py:

@app.get("/api/v1/intelligence/{company}")
async def get_company_intelligence(
    company: str,
    research_depth: str = Query("standard", regex="^(basic|standard|maximum)$"),
    intelligence_type: str = Query("competitive", regex="^(competitive|financial|strategic)$")
):
    """Get cached company intelligence data"""
    try:
        # Use the cache manager we built
        from intelligence_engine.cache.intelligence_cache_manager import cache_manager
        
        data = await cache_manager.get_intelligence(company, research_depth, intelligence_type)
        
        if data:
            return CompanyIntelligence(
                company=company,
                financial_health=data.get('financial_health'),
                competitive_signals=data.get('competitive_signals'), 
                strategic_shifts=data.get('strategic_shifts'),
                cache_hit=True,
                cached_at=data.get('cached_at')
            )
        else:
            return CompanyIntelligence(
                company=company,
                cache_hit=False
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/actions/execute")
async def execute_manual_action(action: ActionRequest):
    """Execute a manual action through the decision orchestrator"""
    try:
        # Create a manual event and trigger decision
        from intelligence_engine.decision_orchestrator import IntelligenceEvent, EventType, Priority
        
        manual_event = IntelligenceEvent(
            event_type=EventType.MANUAL_ACTION,
            priority=Priority.HIGH,
            source='frontend_manual',
            data=action.parameters,
            timestamp=datetime.now()
        )
        
        # Add to decision orchestrator
        pensieve = app.state.pensieve
        await pensieve.decision_orchestrator.add_event(manual_event)
        
        return {"status": "queued", "action": action.action_type}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/dashboard")
async def get_dashboard_data():
    """Get comprehensive dashboard data for frontend"""
    try:
        # Aggregate data from multiple sources
        decisions = await supabase_client.get_decision_history(limit=10)
        system_status = await supabase_client.get_system_status()
        
        # Get intelligence cache stats
        cache_stats = await supabase_client.client.table('intelligence_cache').select(
            'cache_status', count='exact'
        ).execute()
        
        return DashboardData(
            intelligence_cache_stats={
                'total_cached': len(cache_stats.data),
                'cache_hit_rate': 0.85  # Calculate from access patterns
            },
            recent_decisions=decisions,
            system_health=system_status,
            active_jobs=[]  # Get from prefetch queue
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/intelligence/search")
async def search_companies(
    query: str = Query(..., min_length=2),
    limit: int = Query(10, le=50)
):
    """Search cached companies by name or criteria"""
    try:
        response = await supabase_client.client.table('intelligence_cache').select(
            'company_name', 'research_depth', 'intelligence_type', 'cached_at'
        ).ilike('company_name', f'%{query}%').limit(limit).execute()
        
        return {"companies": response.data, "count": len(response.data)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/jobs/active")
async def get_active_jobs():
    """Get currently running intelligence jobs"""
    try:
        response = await supabase_client.client.table('intelligence_prefetch_queue').select('*').in_(
            'status', ['queued', 'processing']
        ).order('priority', desc=True).execute()
        
        return {"jobs": response.data, "count": len(response.data)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/intelligence/prefetch")
async def queue_intelligence_prefetch(
    company: str,
    research_depth: str = "standard",
    intelligence_type: str = "competitive",
    priority: int = Query(50, ge=1, le=100)
):
    """Queue a company for intelligence prefetch"""
    try:
        from intelligence_engine.cache.intelligence_cache_manager import cache_manager
        
        await cache_manager._queue_for_fetch(
            company, research_depth, intelligence_type,
            priority=priority, requested_by='frontend_manual'
        )
        
        return {"status": "queued", "company": company}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket for real-time updates
@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time intelligence and decision updates"""
    await websocket.accept()
    
    try:
        while True:
            # Send real-time updates about:
            # - New intelligence data cached
            # - AI decisions made
            # - System health changes
            # - Job completions
            
            # This would integrate with Redis pub/sub or Supabase real-time
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        pass
