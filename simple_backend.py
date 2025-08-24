#!/usr/bin/env python3
"""
Simple Pensieve Backend Server
Runs the autonomous agent without complex imports
"""

import asyncio
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "intelligence-engine"))

from autonomous_agent import PensieveAutonomousAgent, IntelligenceEvent, EventType, Priority
from datetime import datetime

app = FastAPI(
    title="Pensieve Simple Backend",
    description="Autonomous AI Agent with Vendor Negotiation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None

@app.on_event("startup")
async def startup_event():
    global agent
    agent = PensieveAutonomousAgent()
    print("SUCCESS: Pensieve Autonomous Agent initialized")

@app.get("/")
async def root():
    return {
        "service": "Pensieve Simple Backend",
        "status": "running",
        "description": "Autonomous AI Agent with Real Vendor Negotiations",
        "features": [
            "Autonomous vendor negotiations",
            "IFTTT email integration", 
            "Financial crisis response",
            "40+ business actions",
            "Real-time intelligence"
        ],
        "endpoints": {
            "trigger_negotiation": "/trigger-vendor-negotiation",
            "agent_status": "/agent-status",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent_ready": agent is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/trigger-vendor-negotiation")
async def trigger_vendor_negotiation():
    """Manually trigger vendor negotiation for demo purposes"""
    
    if not agent:
        return {"error": "Agent not initialized"}
    
    # Create financial crisis event
    financial_crisis_event = IntelligenceEvent(
        event_type=EventType.FINANCIAL_CRISIS,
        priority=Priority.CRITICAL,
        data={
            "available_cash": 500000,
            "monthly_expenses": 200000,
            "daily_burn": 6500,
            "runway_days": 77,
            "cash_flow_pressure": 0.85,
            "financial_crisis": True,
            "vendors": ["aws.com", "salesforce.com", "slack.com"],
            "threat_timeline": "60 days"
        },
        source="manual_trigger",
        timestamp=datetime.now(),
        confidence=0.92
    )
    
    # Process the event
    results = await agent.process_intelligence_event(financial_crisis_event)
    
    return {
        "status": "success",
        "message": "Vendor negotiations triggered",
        "actions_executed": len(results),
        "results": [
            {
                "action": result.action_type,
                "success": result.success,
                "message": result.message,
                "impact": result.business_impact
            }
            for result in results
        ]
    }

@app.get("/agent-status") 
async def get_agent_status():
    """Get current agent status and capabilities"""
    
    if not agent:
        return {"error": "Agent not initialized"}
    
    return {
        "agent_ready": True,
        "total_actions": len(agent.actions),
        "action_categories": [
            "Financial Management",
            "Competitive Intelligence", 
            "Customer Relationship",
            "Operational Efficiency",
            "Communication & Outreach"
        ],
        "vendor_negotiation": "enabled",
        "email_system": "IFTTT webhooks",
        "intelligence_sources": ["SixtyFour", "MixRank", "Brex"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)