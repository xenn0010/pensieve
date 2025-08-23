"""
API Extensions for Data Storage and Retrieval
Add these endpoints to main.py for comprehensive data access
"""

from fastapi import HTTPException, Query, Depends
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta

# Pydantic models for API requests/responses
class CompanyResearchRequest(BaseModel):
    company_name: str
    research_type: str = "competitive_analysis"  # competitive_analysis, financial_analysis, etc.
    research_depth: str = "standard"  # basic, standard, comprehensive
    research_questions: Optional[List[str]] = None

class SearchRequest(BaseModel):
    query: str
    search_type: str = "company"  # company, person, technology, market, financial
    search_scope: str = "comprehensive"
    data_sources: Optional[List[str]] = None

class CompanyProfile(BaseModel):
    company_name: str
    company_domain: Optional[str] = None
    industry: Optional[str] = None
    size_category: Optional[str] = None
    financial_metrics: Optional[Dict[str, Any]] = None
    data_quality_score: Optional[float] = None
    last_updated_at: Optional[str] = None

class APICallSummary(BaseModel):
    api_provider: str
    endpoint: str
    call_count: int
    success_rate: float
    avg_duration_ms: float
    last_call_at: str

class ResearchSession(BaseModel):
    id: str
    session_name: Optional[str] = None
    research_objective: str
    research_type: str
    status: str
    started_at: str
    completed_at: Optional[str] = None
    target_companies: List[str]
    key_findings: Optional[Dict[str, Any]] = None

# API ENDPOINTS TO ADD TO main.py:

@app.post("/api/v1/research/start")
async def start_research_session(request: CompanyResearchRequest):
    """Start a new research session for a company"""
    try:
        from intelligence_engine.storage.data_storage_manager import data_storage_manager, ResearchType
        
        # Map string to enum
        research_type_map = {
            "competitive_analysis": ResearchType.COMPETITIVE_ANALYSIS,
            "market_research": ResearchType.MARKET_RESEARCH,
            "due_diligence": ResearchType.DUE_DILIGENCE,
            "financial_analysis": ResearchType.FINANCIAL_ANALYSIS,
            "technology_assessment": ResearchType.TECHNOLOGY_ASSESSMENT
        }
        
        research_type = research_type_map.get(request.research_type, ResearchType.COMPETITIVE_ANALYSIS)
        
        session_id = await data_storage_manager.create_research_session(
            objective=f"Research {request.company_name} for {request.research_type}",
            research_type=research_type,
            target_companies=[request.company_name],
            research_questions=request.research_questions,
            initiated_by="frontend_user",
            automation_level="assisted"
        )
        
        # Trigger intelligence gathering
        from intelligence_engine.cache.intelligence_cache_manager import cache_manager
        
        await cache_manager._queue_for_fetch(
            request.company_name, 
            request.research_depth, 
            "competitive",
            priority=90,
            requested_by=f"research_session:{session_id}"
        )
        
        return {
            "session_id": session_id,
            "status": "started",
            "message": f"Research session started for {request.company_name}",
            "estimated_completion": "5-10 minutes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start research: {str(e)}")

@app.get("/api/v1/research/{session_id}")
async def get_research_session(session_id: str):
    """Get research session details and results"""
    try:
        response = await supabase_client.client.table('research_sessions').select('*').eq('id', session_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Research session not found")
        
        session = response.data[0]
        
        # Get related data
        search_results = []
        if session.get('search_result_ids'):
            search_response = await supabase_client.client.table('search_results').select('*').in_('id', session['search_result_ids']).execute()
            search_results = search_response.data or []
        
        intelligence_findings = []
        if session.get('target_companies'):
            findings_response = await supabase_client.client.table('intelligence_findings').select('*').contains('related_companies', session['target_companies']).execute()
            intelligence_findings = findings_response.data or []
        
        return {
            "session": session,
            "search_results": search_results,
            "intelligence_findings": intelligence_findings,
            "progress": _calculate_research_progress(session)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get research session: {str(e)}")

@app.post("/api/v1/search")
async def perform_search(request: SearchRequest):
    """Perform intelligent search across all data sources"""
    try:
        from intelligence_engine.storage.data_storage_manager import data_storage_manager, SearchType, SearchResult
        
        # Map string to enum
        search_type_map = {
            "company": SearchType.COMPANY,
            "person": SearchType.PERSON,
            "technology": SearchType.TECHNOLOGY,
            "market": SearchType.MARKET,
            "financial": SearchType.FINANCIAL
        }
        
        search_type = search_type_map.get(request.search_type, SearchType.COMPANY)
        
        # Check cache first
        cached_results = await supabase_client.client.table('search_results').select('*').eq(
            'search_query', request.query
        ).eq('search_type', search_type.value).gte(
            'search_timestamp', (datetime.now() - timedelta(hours=6)).isoformat()
        ).order('search_timestamp', desc=True).limit(1).execute()
        
        if cached_results.data:
            # Return cached result
            cached = cached_results.data[0]
            
            # Update access tracking
            await supabase_client.client.table('search_results').update({
                'access_count': cached['access_count'] + 1,
                'last_accessed_at': datetime.now().isoformat()
            }).eq('id', cached['id']).execute()
            
            return {
                "search_id": cached['id'],
                "results": cached['results_data'],
                "total_results": cached['total_results'],
                "confidence_score": cached['confidence_score'],
                "data_sources": cached['data_sources'],
                "cached": True,
                "search_timestamp": cached['search_timestamp']
            }
        
        # Perform new search
        if search_type == SearchType.COMPANY:
            # Use intelligence cache for company searches
            from intelligence_engine.cache.intelligence_cache_manager import cache_manager
            
            intelligence_data = await cache_manager.get_intelligence(
                request.query, "standard", "competitive"
            )
            
            if intelligence_data:
                results_data = intelligence_data
                confidence_score = 0.9
                data_sources = ["intelligence_cache"]
            else:
                # Queue for fetch and return partial results
                results_data = {"status": "queued_for_research", "message": "Company intelligence is being gathered"}
                confidence_score = 0.5
                data_sources = ["queue"]
        else:
            # For other search types, perform basic search
            results_data = {"message": f"Search for {request.query} completed", "type": search_type.value}
            confidence_score = 0.7
            data_sources = ["internal"]
        
        # Store search result
        search_result = SearchResult(
            query=request.query,
            search_type=search_type,
            results_data=results_data,
            confidence_score=confidence_score,
            data_sources=data_sources,
            total_results=len(results_data) if isinstance(results_data, list) else 1
        )
        
        search_id = await data_storage_manager.store_search_result(
            search_result=search_result,
            requested_by="frontend_user"
        )
        
        return {
            "search_id": search_id,
            "results": results_data,
            "total_results": search_result.total_results,
            "confidence_score": confidence_score,
            "data_sources": data_sources,
            "cached": False,
            "search_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/api/v1/companies/{company_name}/profile")
async def get_company_profile(company_name: str):
    """Get comprehensive company profile"""
    try:
        from intelligence_engine.storage.data_storage_manager import data_storage_manager
        
        # Get comprehensive research data
        research_data = await data_storage_manager.get_company_research_data(company_name)
        
        if not research_data.get('profile'):
            # Create basic profile if none exists
            profile = {
                "company_name": company_name,
                "data_sources": [],
                "last_updated_at": datetime.now().isoformat(),
                "data_quality_score": 0.0,
                "times_researched": 0
            }
        else:
            profile = research_data['profile']
        
        return {
            "profile": profile,
            "recent_searches": research_data.get('recent_searches', []),
            "research_sessions": research_data.get('research_sessions', []),
            "intelligence_findings": research_data.get('intelligence_findings', []),
            "cached_intelligence": research_data.get('cached_intelligence', []),
            "data_completeness": _calculate_data_completeness(research_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get company profile: {str(e)}")

@app.get("/api/v1/analytics/api-usage")
async def get_api_usage_analytics(
    hours_back: int = Query(24, ge=1, le=168),
    provider: Optional[str] = None
):
    """Get API usage analytics"""
    try:
        # Base query
        query = supabase_client.client.table('api_call_results').select('*').gte(
            'request_timestamp', (datetime.now() - timedelta(hours=hours_back)).isoformat()
        )
        
        if provider:
            query = query.eq('api_provider', provider)
        
        response = await query.execute()
        api_calls = response.data or []
        
        # Calculate analytics
        total_calls = len(api_calls)
        successful_calls = len([call for call in api_calls if 200 <= call['response_status'] < 300])
        failed_calls = total_calls - successful_calls
        
        # Group by provider
        provider_stats = {}
        for call in api_calls:
            provider_name = call['api_provider']
            if provider_name not in provider_stats:
                provider_stats[provider_name] = {
                    'total_calls': 0,
                    'successful_calls': 0,
                    'avg_duration_ms': 0,
                    'total_duration_ms': 0
                }
            
            provider_stats[provider_name]['total_calls'] += 1
            if 200 <= call['response_status'] < 300:
                provider_stats[provider_name]['successful_calls'] += 1
            
            if call.get('duration_ms'):
                provider_stats[provider_name]['total_duration_ms'] += call['duration_ms']
        
        # Calculate averages
        for stats in provider_stats.values():
            if stats['total_calls'] > 0:
                stats['avg_duration_ms'] = stats['total_duration_ms'] / stats['total_calls']
                stats['success_rate'] = stats['successful_calls'] / stats['total_calls']
        
        return {
            "summary": {
                "total_calls": total_calls,
                "successful_calls": successful_calls,
                "failed_calls": failed_calls,
                "success_rate": successful_calls / total_calls if total_calls > 0 else 0,
                "hours_analyzed": hours_back
            },
            "by_provider": provider_stats,
            "recent_calls": api_calls[-10:] if api_calls else []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get API analytics: {str(e)}")

@app.get("/api/v1/analytics/data-quality")
async def get_data_quality_metrics():
    """Get data quality and completeness metrics"""
    try:
        # Get recent intelligence cache entries
        cache_response = await supabase_client.client.table('intelligence_cache').select('*').eq(
            'cache_status', 'completed'
        ).order('cached_at', desc=True).limit(100).execute()
        
        cache_entries = cache_response.data or []
        
        # Calculate quality metrics
        total_entries = len(cache_entries)
        if total_entries == 0:
            return {"message": "No cached intelligence data available"}
        
        # Data completeness analysis
        completeness_scores = []
        quality_scores = []
        
        for entry in cache_entries:
            # Count non-null data fields
            data_fields = [
                'financial_health', 'competitive_signals', 'strategic_shifts',
                'customer_intelligence', 'market_opportunities'
            ]
            
            non_null_fields = sum(1 for field in data_fields if entry.get(field))
            completeness = non_null_fields / len(data_fields)
            completeness_scores.append(completeness)
            
            # Quality based on data size and fetch time
            data_size = entry.get('data_size_bytes', 0)
            fetch_time = entry.get('fetch_duration_seconds', 0)
            
            quality = min(1.0, (data_size / 5000) + (1.0 if fetch_time < 120 else 0.5))
            quality_scores.append(quality)
        
        avg_completeness = sum(completeness_scores) / len(completeness_scores)
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        # Company coverage analysis
        companies_with_data = len(set(entry['company_name'] for entry in cache_entries))
        
        return {
            "data_quality": {
                "avg_completeness_score": round(avg_completeness, 3),
                "avg_quality_score": round(avg_quality, 3),
                "total_cached_companies": companies_with_data,
                "total_cache_entries": total_entries
            },
            "completeness_distribution": {
                "high_completeness": len([s for s in completeness_scores if s >= 0.8]),
                "medium_completeness": len([s for s in completeness_scores if 0.4 <= s < 0.8]),
                "low_completeness": len([s for s in completeness_scores if s < 0.4])
            },
            "data_freshness": {
                "entries_last_24h": len([e for e in cache_entries if 
                    datetime.fromisoformat(e['cached_at'].replace('Z', '+00:00')).replace(tzinfo=None) 
                    >= datetime.now() - timedelta(hours=24)
                ]),
                "entries_last_week": len([e for e in cache_entries if 
                    datetime.fromisoformat(e['cached_at'].replace('Z', '+00:00')).replace(tzinfo=None) 
                    >= datetime.now() - timedelta(days=7)
                ])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get data quality metrics: {str(e)}")

# Helper functions
def _calculate_research_progress(session: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate research session progress"""
    
    total_steps = 5  # Define research steps
    completed_steps = 0
    
    if session.get('search_result_ids'):
        completed_steps += 1
    if session.get('api_call_ids'):
        completed_steps += 1
    if session.get('key_findings'):
        completed_steps += 1
    if session.get('data_summary'):
        completed_steps += 1
    if session.get('status') == 'completed':
        completed_steps = total_steps
    
    progress_percent = (completed_steps / total_steps) * 100
    
    return {
        "progress_percent": progress_percent,
        "completed_steps": completed_steps,
        "total_steps": total_steps,
        "status": session.get('status', 'active'),
        "estimated_completion": "5-10 minutes" if progress_percent < 80 else "Complete"
    }

def _calculate_data_completeness(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate data completeness for a company"""
    
    profile = research_data.get('profile', {})
    
    # Define data categories and check completeness
    categories = {
        'basic_info': ['company_name', 'industry', 'headquarters_location'],
        'financial_data': ['financial_metrics'],
        'team_data': ['employee_metrics'],
        'technology_data': ['technology_stack'],
        'market_data': ['competitive_position', 'market_presence']
    }
    
    completeness = {}
    
    for category, fields in categories.items():
        available_fields = sum(1 for field in fields if profile.get(field))
        completeness[category] = {
            'score': available_fields / len(fields),
            'available_fields': available_fields,
            'total_fields': len(fields)
        }
    
    # Overall completeness
    total_available = sum(c['available_fields'] for c in completeness.values())
    total_possible = sum(c['total_fields'] for c in completeness.values())
    
    overall_score = total_available / total_possible if total_possible > 0 else 0
    
    return {
        'overall_score': round(overall_score, 3),
        'by_category': completeness,
        'data_sources_count': len(profile.get('data_sources', [])),
        'last_updated': profile.get('last_updated_at'),
        'research_count': profile.get('times_researched', 0)
    }
