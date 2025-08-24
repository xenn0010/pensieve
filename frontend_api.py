#!/usr/bin/env python3
"""
Pensieve Frontend API Server
API endpoints specifically designed for frontend data visualization and interaction
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Path, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field
import uvicorn
import asyncio
import random
import uuid

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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agent instance
agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup for the FastAPI app"""
    global agent
    logger.info("Initializing Pensieve Frontend API...")
    agent = PensieveAutonomousAgent()
    logger.info(f"Frontend API ready with {len(agent.actions)} autonomous actions")
    yield

# Initialize FastAPI app
app = FastAPI(
    title="Pensieve Frontend API",
    description="Frontend API for Pensieve Autonomous Intelligence Dashboard",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Pydantic models for frontend
class CompanyResearchRequest(BaseModel):
    company_domain: str = Field(..., description="Company domain to research")
    research_depth: str = Field("standard", description="Research depth: quick, standard, deep")
    include_competitors: bool = Field(True, description="Include competitor analysis")

class AgentQueryRequest(BaseModel):
    query: str = Field(..., description="Question to ask the agent")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    company_focus: Optional[str] = Field(None, description="Company to focus analysis on")

class DashboardDataResponse(BaseModel):
    total_companies_analyzed: int
    active_intelligence_signals: int
    actions_executed_today: int
    cache_hit_rate: float
    top_insights: List[Dict[str, Any]]
    recent_actions: List[Dict[str, Any]]

class CompanyIntelligenceResponse(BaseModel):
    company: str
    financial_health: str
    employee_count: Optional[int]
    technology_stack: List[str]
    risk_factors: List[str]
    opportunities: List[str]
    competitive_position: str
    intelligence_confidence: float
    last_updated: str

class MarketInsightResponse(BaseModel):
    insight_type: str
    title: str
    description: str
    companies_affected: List[str]
    impact_score: float
    recommended_actions: List[str]
    data_sources: List[str]
    timestamp: str

# Financial Data Endpoints
@app.get("/financial/kpis")
async def get_financial_kpis():
    """Get real-time financial KPIs for dashboard"""
    # Mock data for hackathon demo
    return {
        "runway_months": 18.5,
        "cash_on_hand": 2400000,
        "monthly_burn": 130000,
        "scenario": "healthy_saas",
        "last_updated": datetime.now().isoformat(),
        "trends": {
            "runway_change": 2.3,
            "cash_change": -0.8,
            "burn_change": 0
        }
    }

@app.get("/financial/transactions")
async def get_financial_transactions():
    """Get company financial transactions (not market deals)"""
    # Mock company financial data for hackathon demo
    return {
        "transactions": [
            {
                "id": "fin_001",
                "type": "expense",
                "amount": -50000,
                "currency": "USD",
                "description": "AWS Cloud Services - January",
                "category": "infrastructure",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "status": "completed",
                "merchant": "Amazon Web Services"
            },
            {
                "id": "fin_002",
                "type": "revenue",
                "amount": 150000,
                "currency": "USD",
                "description": "Enterprise License Renewal",
                "category": "revenue",
                "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
                "status": "completed",
                "merchant": "TechCorp Inc"
            },
            {
                "id": "fin_003",
                "type": "expense",
                "amount": -80000,
                "currency": "USD",
                "description": "Employee Salaries - January",
                "category": "payroll",
                "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
                "status": "completed",
                "merchant": "Payroll System"
            },
            {
                "id": "fin_004",
                "type": "expense",
                "amount": -25000,
                "currency": "USD",
                "description": "Office Rent - January",
                "category": "facilities",
                "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(),
                "status": "completed",
                "merchant": "OfficeSpace Inc"
            },
            {
                "id": "fin_005",
                "type": "revenue",
                "amount": 75000,
                "currency": "USD",
                "description": "Consulting Services",
                "category": "revenue",
                "timestamp": (datetime.now() - timedelta(hours=12)).isoformat(),
                "status": "completed",
                "merchant": "ConsultCorp"
            }
        ],
        "summary": {
            "total_revenue": 225000,
            "total_expenses": 155000,
            "net_cash_flow": 70000,
            "transaction_count": 5
        }
    }

@app.get("/financial/scenarios")
async def get_financial_scenarios():
    """Get available financial scenarios for demo"""
    return {
        "scenarios": [
            {
                "id": "healthy_saas",
                "name": "Healthy SaaS",
                "description": "Strong growth, good runway",
                "runway_months": 18.5,
                "cash_on_hand": 2400000,
                "monthly_burn": 130000,
                "status": "active"
            },
            {
                "id": "cash_crunch",
                "name": "Cash Crunch",
                "description": "Low runway, need funding",
                "runway_months": 3.2,
                "cash_on_hand": 420000,
                "monthly_burn": 130000,
                "status": "available"
            },
            {
                "id": "rapid_burn",
                "name": "Rapid Burn",
                "description": "High burn rate, scaling issues",
                "runway_months": 8.1,
                "cash_on_hand": 1050000,
                "monthly_burn": 130000,
                "status": "available"
            },
            {
                "id": "seasonal_business",
                "name": "Seasonal Business",
                "description": "Variable revenue patterns",
                "runway_months": 12.3,
                "cash_on_hand": 1600000,
                "monthly_burn": 130000,
                "status": "available"
            }
        ]
    }

@app.post("/financial/scenario/{scenario_id}")
async def switch_financial_scenario(scenario_id: str):
    """Switch to a different financial scenario for demo"""
    scenarios = {
        "healthy_saas": {
            "runway_months": 18.5,
            "cash_on_hand": 2400000,
            "monthly_burn": 130000,
            "description": "Strong growth, good runway"
        },
        "cash_crunch": {
            "runway_months": 3.2,
            "cash_on_hand": 420000,
            "monthly_burn": 130000,
            "description": "Low runway, need funding"
        },
        "rapid_burn": {
            "runway_months": 8.1,
            "cash_on_hand": 1050000,
            "monthly_burn": 130000,
            "description": "High burn rate, scaling issues"
        },
        "seasonal_business": {
            "runway_months": 12.3,
            "cash_on_hand": 1600000,
            "monthly_burn": 130000,
            "description": "Variable revenue patterns"
        }
    }
    
    if scenario_id not in scenarios:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return {
        "message": f"Switched to {scenario_id} scenario",
        "scenario": scenarios[scenario_id],
        "timestamp": datetime.now().isoformat()
    }

# Dashboard Data Endpoints
@app.get("/dashboard/overview", response_model=DashboardDataResponse)
async def get_dashboard_overview():
    """Get overview data for the main dashboard"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    # Mock data for dashboard - in production, pull from database
    return DashboardDataResponse(
        total_companies_analyzed=len(data_cache._cache),
        active_intelligence_signals=12,
        actions_executed_today=24,
        cache_hit_rate=0.85,
        top_insights=[
            {
                "title": "Competitor Distress Detected",
                "company": "TechCorp Inc",
                "impact": "High",
                "confidence": 0.87
            },
            {
                "title": "Customer Churn Risk",
                "company": "Enterprise Client",
                "impact": "Critical",
                "confidence": 0.92
            }
        ],
        recent_actions=[
            {
                "action": "talent_poaching",
                "target": "competitor-xyz.com",
                "status": "completed",
                "impact": "$450K talent value"
            },
            {
                "action": "churn_prevention", 
                "target": "enterprise_client_001",
                "status": "in_progress",
                "impact": "$850K contract saved"
            }
        ]
    )

@app.get("/dashboard/metrics")
async def get_dashboard_metrics():
    """Get real-time metrics for dashboard widgets"""
    return {
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
            "total_entries": len(data_cache._cache),
            "hit_rate": 0.85,
            "avg_response_time": "1.2s"
        }
    }

# Company Research Endpoints
@app.post("/research/company", response_model=CompanyIntelligenceResponse)
async def research_company(request: CompanyResearchRequest):
    """Research a company and return comprehensive intelligence"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # Get sample action to access intelligence methods
        sample_action = next(iter(agent.actions.values()))
        
        # Fetch intelligence data
        financial_data = await sample_action.fetch_sixtyfour_data(request.company_domain)
        tech_data = await sample_action.fetch_mixrank_data(request.company_domain)
        
        # Extract key information
        company_analysis = financial_data.get("company_analysis", {})
        
        # Process technology stack
        ios_apps = tech_data.get("ios_apps", {}).get("data", [])
        android_apps = tech_data.get("android_apps", {}).get("data", [])
        tech_stack = [app.get("name", "Unknown") for app in ios_apps + android_apps][:10]
        
        return CompanyIntelligenceResponse(
            company=request.company_domain,
            financial_health=company_analysis.get("financial_health", "unknown"),
            employee_count=company_analysis.get("employee_count"),
            technology_stack=tech_stack,
            risk_factors=company_analysis.get("risk_factors", []),
            opportunities=company_analysis.get("growth_indicators", []),
            competitive_position=company_analysis.get("market_position", "unknown"),
            intelligence_confidence=0.85,
            last_updated=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Company research failed for {request.company_domain}: {e}")
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

@app.get("/research/companies")
async def get_researched_companies():
    """Get list of previously researched companies"""
    # Extract company domains from cache
    companies = []
    for cache_key in data_cache._cache.keys():
        if cache_key.startswith(("sixtyfour_", "mixrank_")):
            company = cache_key.split("_", 1)[1]
            if company not in companies:
                companies.append(company)
    
    return {
        "companies": companies,
        "total": len(companies),
        "last_updated": datetime.now().isoformat()
    }

@app.get("/research/company/{company_domain}/competitors")
async def get_company_competitors(company_domain: str = Path(...)):
    """Get competitor analysis for a specific company"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    # Mock competitor data - in production, use real competitor detection
    competitors = [
        {
            "company": "competitor-a.com",
            "similarity_score": 0.85,
            "financial_health": "stable",
            "threat_level": "medium",
            "opportunities": ["talent_acquisition", "market_share_capture"]
        },
        {
            "company": "competitor-b.com", 
            "similarity_score": 0.72,
            "financial_health": "declining",
            "threat_level": "low",
            "opportunities": ["acquisition_target", "talent_poaching"]
        }
    ]
    
    return {
        "target_company": company_domain,
        "competitors": competitors,
        "analysis_date": datetime.now().isoformat()
    }

# Agent Query/Chat Endpoints
@app.post("/agent/query")
async def query_agent(request: AgentQueryRequest):
    """Ask the agent a question and get intelligent response"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # Create a mock intelligence event based on the query
        query_event = IntelligenceEvent(
            event_type=EventType.MARKET_OPPORTUNITY,
            priority=Priority.MEDIUM,
            data={
                "query": request.query,
                "context": request.context or {},
                "company_focus": request.company_focus
            },
            source="user_query",
            timestamp=datetime.now(),
            confidence=0.8
        )
        
        # Use Gemini to generate response
        prompt = f"""
        You are Pensieve, an Autonomous Chief Intelligence Officer. A user has asked you this question:
        
        "{request.query}"
        
        Context: {json.dumps(request.context or {}, indent=2)}
        Company Focus: {request.company_focus or "None"}
        
        Provide a comprehensive, actionable response based on your intelligence capabilities.
        If relevant, suggest specific autonomous actions that could be executed.
        """
        
        response = await agent.model.generate_content_async(prompt)
        agent_response = response.text
        
        # Suggest relevant actions based on query content
        suggested_actions = []
        query_lower = request.query.lower()
        
        if any(word in query_lower for word in ["competitor", "competition", "rival"]):
            suggested_actions.extend(["competitive_intelligence_gathering", "talent_poaching", "acquisition_evaluation"])
        
        if any(word in query_lower for word in ["customer", "churn", "retention"]):
            suggested_actions.extend(["churn_prevention", "customer_health_scoring", "customer_success_intervention"])
        
        if any(word in query_lower for word in ["financial", "cash", "funding", "money"]):
            suggested_actions.extend(["expense_optimization", "cash_flow_optimization", "funding_preparation"])
        
        return {
            "query": request.query,
            "response": agent_response,
            "suggested_actions": suggested_actions[:5],
            "confidence": 0.85,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Agent query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/agent/capabilities")
async def get_agent_capabilities():
    """Get agent capabilities organized by category"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    capabilities = {
        "financial_actions": {
            "count": 8,
            "actions": [
                "Emergency Cash Management",
                "Expense Optimization", 
                "Funding Preparation",
                "Credit Line Activation",
                "Vendor Contract Renegotiation",
                "Cash Flow Optimization",
                "Emergency Budget Cuts",
                "Accounts Receivable Acceleration"
            ]
        },
        "competitive_actions": {
            "count": 8,
            "actions": [
                "Talent Poaching",
                "Acquisition Evaluation",
                "Pricing Strategy Adjustment",
                "Feature Gap Analysis", 
                "Market Positioning Shift",
                "Competitive Intelligence Gathering",
                "Counter-Acquisition Strategy",
                "Talent Retention Defense"
            ]
        },
        "customer_actions": {
            "count": 8,
            "actions": [
                "Churn Prevention",
                "Customer Health Scoring",
                "Contract Renegotiation",
                "Satisfaction Survey",
                "Upsell Opportunity Mining",
                "Customer Success Intervention",
                "Loyalty Program Launch",
                "Proactive Support Outreach"
            ]
        },
        "operational_actions": {
            "count": 8,
            "actions": [
                "Security Audit",
                "Team Restructuring", 
                "Vendor Contract Review",
                "Compliance Preparation",
                "Process Optimization",
                "Resource Reallocation",
                "Emergency Response Plan",
                "Operational Efficiency Analysis"
            ]
        },
        "communication_actions": {
            "count": 8,
            "actions": [
                "Crisis Communication",
                "Stakeholder Notification",
                "Media Response",
                "Internal Communication",
                "Customer Communication",
                "Investor Update",
                "Social Media Response",
                "Reputation Management"
            ]
        }
    }
    
    return {
        "total_actions": 40,
        "categories": capabilities,
        "intelligence_sources": ["SixtyFour", "MixRank", "Brex", "Pylon"],
        "autonomous_execution": True
    }

# Intelligence and Insights Endpoints
@app.get("/intelligence/insights", response_model=List[MarketInsightResponse])
async def get_market_insights():
    """Get current market insights and intelligence signals"""
    # Mock insights - in production, pull from intelligence processing
    insights = [
        MarketInsightResponse(
            insight_type="competitor_distress",
            title="Digital Exodus at TechCorp",
            description="Competitor showing signs of major layoffs affecting 200+ employees",
            companies_affected=["techcorp.com"],
            impact_score=0.87,
            recommended_actions=["talent_poaching", "acquisition_evaluation", "market_positioning_shift"],
            data_sources=["sixtyfour", "mixrank"],
            timestamp=datetime.now().isoformat()
        ),
        MarketInsightResponse(
            insight_type="customer_risk",
            title="Enterprise Client Churn Risk",
            description="High-value customer showing 92% churn probability",
            companies_affected=["enterprise-client.com"],
            impact_score=0.92,
            recommended_actions=["churn_prevention", "customer_success_intervention", "contract_renegotiation"],
            data_sources=["pylon"],
            timestamp=(datetime.now() - timedelta(hours=2)).isoformat()
        ),
        MarketInsightResponse(
            insight_type="market_opportunity",
            title="Vendor Negotiation Opportunity",
            description="Key vendor showing financial distress - negotiation leverage available",
            companies_affected=["vendor-xyz.com"],
            impact_score=0.75,
            recommended_actions=["vendor_contract_renegotiation", "cash_flow_optimization"],
            data_sources=["sixtyfour"],
            timestamp=(datetime.now() - timedelta(hours=4)).isoformat()
        )
    ]
    
    return insights

@app.get("/intelligence/signals")
async def get_intelligence_signals():
    """Get active intelligence signals by type"""
    return {
        "active_signals": {
            "competitor_distress": 3,
            "customer_churn_risk": 2,
            "financial_crisis": 1,
            "market_opportunity": 5,
            "security_threat": 0,
            "regulatory_change": 1
        },
        "signal_history": [
            {"type": "competitor_distress", "count": 3, "date": datetime.now().date().isoformat()},
            {"type": "customer_churn_risk", "count": 5, "date": (datetime.now() - timedelta(days=1)).date().isoformat()},
            {"type": "market_opportunity", "count": 2, "date": (datetime.now() - timedelta(days=2)).date().isoformat()}
        ],
        "total_processed_today": 24,
        "autonomous_actions_triggered": 12
    }

# Action Execution Endpoints for Frontend
@app.get("/actions/recent")
async def get_recent_actions():
    """Get recently executed actions for the activity feed"""
    # Mock recent actions - in production, pull from database
    recent_actions = [
        {
            "id": "act_001",
            "action_type": "talent_poaching",
            "target": "competitor-xyz.com",
            "status": "completed",
            "business_impact": "$450K talent value acquired",
            "execution_time": "2.3s",
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.87
        },
        {
            "id": "act_002", 
            "action_type": "churn_prevention",
            "target": "enterprise-client.com",
            "status": "in_progress",
            "business_impact": "$850K contract at risk",
            "execution_time": "1.8s",
            "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "confidence": 0.92
        },
        {
            "id": "act_003",
            "action_type": "vendor_contract_renegotiation",
            "target": "multiple vendors",
            "status": "completed",
            "business_impact": "$125K annual savings",
            "execution_time": "4.1s",
            "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
            "confidence": 0.78
        }
    ]
    
    return {
        "recent_actions": recent_actions,
        "total_today": len(recent_actions) + 21,
        "success_rate": 0.96
    }

@app.get("/actions/performance")
async def get_action_performance():
    """Get action performance analytics"""
    return {
        "performance_by_category": {
            "financial": {"executed": 45, "success_rate": 0.94, "avg_roi": 125000},
            "competitive": {"executed": 38, "success_rate": 0.89, "avg_roi": 200000},
            "customer": {"executed": 52, "success_rate": 0.91, "avg_roi": 180000},
            "operational": {"executed": 29, "success_rate": 0.87, "avg_roi": 95000},
            "communication": {"executed": 24, "success_rate": 0.92, "avg_roi": 75000}
        },
        "top_performing_actions": [
            {"action": "talent_poaching", "success_rate": 0.95, "avg_roi": 250000},
            {"action": "churn_prevention", "success_rate": 0.89, "avg_roi": 220000},
            {"action": "vendor_contract_renegotiation", "success_rate": 0.87, "avg_roi": 150000}
        ],
        "execution_trends": {
            "daily_average": 28,
            "weekly_trend": "+12%",
            "monthly_total": 756
        }
    }

# WebSocket for real-time financial updates
@app.websocket("/ws/financial")
async def financial_websocket(websocket: WebSocket):
    """Real-time financial data updates for demo"""
    await websocket.accept()
    
    try:
        # Simulate real-time financial updates every 5 seconds
        while True:
            # Generate mock real-time data
            current_time = datetime.now()
            
            # Simulate small changes in financial data
            mock_update = {
                "type": "financial_update",
                "timestamp": current_time.isoformat(),
                "data": {
                    "cash_on_hand": 2400000 + random.randint(-5000, 5000),
                    "runway_months": 18.5 + random.uniform(-0.1, 0.1),
                    "monthly_burn": 130000 + random.randint(-1000, 1000),
                    "new_transaction": {
                        "id": f"live_{uuid.uuid4().hex[:8]}",
                        "type": random.choice(["expense", "revenue"]),
                        "amount": random.randint(1000, 50000) * (1 if random.choice([True, False]) else -1),
                        "description": random.choice([
                            "Cloud Service Usage",
                            "Software License",
                            "Consulting Fee",
                            "Office Supplies"
                        ]),
                        "timestamp": current_time.isoformat()
                    }
                }
            }
            
            await websocket.send_text(json.dumps(mock_update))
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except WebSocketDisconnect:
        print("Financial WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")

# Real-time data endpoints
@app.get("/realtime/status")
async def get_realtime_status():
    """Get real-time system status"""
    return {
        "agent_status": "operational",
        "active_processes": 3,
        "queue_length": 2,
        "last_intelligence_update": (datetime.now() - timedelta(minutes=2)).isoformat(),
        "system_load": 0.45,
        "memory_usage": 0.62
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check for frontend API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agent_ready": agent is not None,
        "api_version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Pensieve Frontend API",
        "version": "1.0.0", 
        "description": "Frontend API for Pensieve Autonomous Intelligence Dashboard",
        "endpoints": {
            "dashboard": "/dashboard/*",
            "research": "/research/*",
            "agent": "/agent/*",
            "intelligence": "/intelligence/*",
            "actions": "/actions/*"
        },
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "frontend_api:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )