#!/usr/bin/env python3
"""
Pensieve Autonomous Agent API Server
Production-ready FastAPI backend for autonomous business intelligence agent
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field
import uvicorn

from autonomous_agent import (
    PensieveAutonomousAgent, 
    IntelligenceEvent, 
    EventType, 
    Priority,
    ActionResult,
    data_cache
)
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global agent instance
agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup for the FastAPI app"""
    global agent
    logger.info("Initializing Pensieve Autonomous Agent...")
    agent = PensieveAutonomousAgent()
    logger.info(f"Agent initialized with {len(agent.actions)} autonomous actions")
    yield
    logger.info("Shutting down Pensieve Autonomous Agent")

# Initialize FastAPI app
app = FastAPI(
    title="Pensieve Autonomous Agent API",
    description="Production API for the world's first Autonomous Chief Intelligence Officer",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Pydantic models for API
class IntelligenceEventRequest(BaseModel):
    event_type: str = Field(..., description="Type of intelligence event")
    priority: str = Field(..., description="Event priority level")
    data: Dict[str, Any] = Field(..., description="Event data payload")
    source: str = Field(..., description="Data source (sixtyfour, mixrank, pylon, brex)")
    confidence: float = Field(0.8, ge=0.0, le=1.0, description="Confidence score")

class ActionExecutionRequest(BaseModel):
    action_type: str = Field(..., description="Action to execute")
    event_data: Dict[str, Any] = Field(..., description="Event data for action")
    force_execution: bool = Field(False, description="Force execution regardless of confidence")

class AgentStatusResponse(BaseModel):
    status: str
    total_actions: int
    cache_size: int
    uptime_seconds: float
    version: str

class IntelligenceEventResponse(BaseModel):
    event_id: str
    actions_executed: int
    execution_time: float
    results: List[Dict[str, Any]]
    status: str

class ActionResultResponse(BaseModel):
    success: bool
    action_type: str
    message: str
    business_impact: Optional[Dict[str, Any]]
    execution_time: float
    cost: float

class MarketIntelligenceRequest(BaseModel):
    company_domain: str = Field(..., description="Company domain to analyze")
    intelligence_types: List[str] = Field(["financial", "technology"], description="Types of intelligence to gather")
    use_cache: bool = Field(True, description="Use cached data if available")

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agent_ready": agent is not None,
        "version": "1.0.0"
    }

# Agent status endpoint
@app.get("/status", response_model=AgentStatusResponse)
async def get_agent_status():
    """Get current agent status and metrics"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    return AgentStatusResponse(
        status="operational",
        total_actions=len(agent.actions),
        cache_size=len(data_cache._cache),
        uptime_seconds=0.0,  # Calculate based on start time
        version="1.0.0"
    )

# List available actions
@app.get("/actions")
async def list_actions():
    """List all available autonomous actions"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    actions_info = {}
    for name, action in agent.actions.items():
        actions_info[name] = {
            "name": name,
            "description": action.system_prompt[:200] + "..." if len(action.system_prompt) > 200 else action.system_prompt,
            "category": _get_action_category(name)
        }
    
    return {
        "total_actions": len(actions_info),
        "actions": actions_info
    }

def _get_action_category(action_name: str) -> str:
    """Get category for an action"""
    financial_actions = ["emergency_cash_transfer", "expense_optimization", "funding_preparation", 
                        "credit_line_activation", "vendor_contract_renegotiation", "cash_flow_optimization",
                        "emergency_budget_cuts", "accounts_receivable_acceleration"]
    
    competitive_actions = ["talent_poaching", "acquisition_evaluation", "pricing_strategy_adjustment",
                          "feature_gap_analysis", "market_positioning_shift", "competitive_intelligence_gathering",
                          "counter_acquisition_strategy", "talent_retention_defense"]
    
    customer_actions = ["churn_prevention", "customer_health_scoring", "contract_renegotiation",
                       "satisfaction_survey", "upsell_opportunity_mining", "customer_success_intervention",
                       "loyalty_program_launch", "proactive_support_outreach"]
    
    operational_actions = ["security_audit", "team_restructuring", "vendor_contract_review",
                          "compliance_preparation", "process_optimization", "resource_reallocation",
                          "emergency_response_plan", "operational_efficiency_analysis"]
    
    communication_actions = ["crisis_communication", "stakeholder_notification", "media_response",
                            "internal_communication", "customer_communication", "investor_update",
                            "social_media_response", "reputation_management"]
    
    if action_name in financial_actions:
        return "financial"
    elif action_name in competitive_actions:
        return "competitive"
    elif action_name in customer_actions:
        return "customer"
    elif action_name in operational_actions:
        return "operational"
    elif action_name in communication_actions:
        return "communication"
    else:
        return "unknown"

# Process intelligence event
@app.post("/intelligence/event", response_model=IntelligenceEventResponse)
async def process_intelligence_event(event_request: IntelligenceEventRequest, background_tasks: BackgroundTasks):
    """Process an intelligence event and execute autonomous actions"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # Validate event type
        try:
            event_type = EventType(event_request.event_type.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid event type: {event_request.event_type}")
        
        # Validate priority
        try:
            priority = Priority(event_request.priority.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid priority: {event_request.priority}")
        
        # Create intelligence event
        intelligence_event = IntelligenceEvent(
            event_type=event_type,
            priority=priority,
            data=event_request.data,
            source=event_request.source,
            timestamp=datetime.now(),
            confidence=event_request.confidence
        )
        
        # Process event
        start_time = datetime.now()
        results = await agent.process_intelligence_event(intelligence_event)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Generate event ID
        event_id = f"evt_{int(datetime.now().timestamp())}"
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "action_type": result.action_type,
                "success": result.success,
                "message": result.message,
                "business_impact": result.business_impact,
                "execution_time": result.execution_time,
                "cost": result.cost
            })
        
        logger.info(f"Processed intelligence event {event_id}: {len(results)} actions executed")
        
        return IntelligenceEventResponse(
            event_id=event_id,
            actions_executed=len(results),
            execution_time=execution_time,
            results=formatted_results,
            status="completed"
        )
        
    except Exception as e:
        logger.error(f"Failed to process intelligence event: {e}")
        raise HTTPException(status_code=500, detail=f"Event processing failed: {str(e)}")

# Execute single action
@app.post("/actions/execute", response_model=ActionResultResponse)
async def execute_action(action_request: ActionExecutionRequest):
    """Execute a single autonomous action"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if action_request.action_type not in agent.actions:
        raise HTTPException(status_code=404, detail=f"Action not found: {action_request.action_type}")
    
    try:
        action = agent.actions[action_request.action_type]
        result = await action.execute(action_request.event_data)
        
        logger.info(f"Executed action {action_request.action_type}: {'SUCCESS' if result.success else 'FAILED'}")
        
        return ActionResultResponse(
            success=result.success,
            action_type=result.action_type,
            message=result.message,
            business_impact=result.business_impact,
            execution_time=result.execution_time,
            cost=result.cost
        )
        
    except Exception as e:
        logger.error(f"Action execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Action execution failed: {str(e)}")

# Get market intelligence
@app.post("/intelligence/market")
async def get_market_intelligence(request: MarketIntelligenceRequest):
    """Fetch market intelligence for a company"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        intelligence_data = {}
        
        # Get first available action to access intelligence methods
        sample_action = next(iter(agent.actions.values()))
        
        if "financial" in request.intelligence_types:
            financial_data = await sample_action.fetch_sixtyfour_data(request.company_domain)
            intelligence_data["financial"] = financial_data
        
        if "technology" in request.intelligence_types:
            tech_data = await sample_action.fetch_mixrank_data(request.company_domain)
            intelligence_data["technology"] = tech_data
        
        return {
            "company": request.company_domain,
            "intelligence_types": request.intelligence_types,
            "data": intelligence_data,
            "timestamp": datetime.now().isoformat(),
            "cached": request.use_cache and bool(intelligence_data)
        }
        
    except Exception as e:
        logger.error(f"Market intelligence fetch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Intelligence fetch failed: {str(e)}")

# Get cache statistics
@app.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    return {
        "total_entries": len(data_cache._cache),
        "timestamps": list(data_cache._timestamps.keys()),
        "ttl_seconds": data_cache.ttl
    }

# Clear cache
@app.delete("/cache")
async def clear_cache():
    """Clear the intelligence cache"""
    data_cache._cache.clear()
    data_cache._timestamps.clear()
    logger.info("Intelligence cache cleared")
    return {"message": "Cache cleared successfully"}

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "agent_status": "operational" if agent else "not_initialized",
        "total_actions": len(agent.actions) if agent else 0,
        "cache_entries": len(data_cache._cache),
        "timestamp": datetime.now().isoformat()
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Pensieve Autonomous Agent API",
        "version": "1.0.0",
        "description": "Production API for the world's first Autonomous Chief Intelligence Officer",
        "documentation": "/docs",
        "health_check": "/health",
        "total_actions": len(agent.actions) if agent else 0
    }

if __name__ == "__main__":
    # Production configuration
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1,
        log_level="info",
        access_log=True,
        server_header=False,
        date_header=False
    )