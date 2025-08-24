from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Create FastAPI app
app = FastAPI(
    title="Runway Navigator Financial API",
    description="Simple financial API for hackathon demo",
    version="1.0.0"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Financial Data Models
class FinancialKPIs(BaseModel):
    runway_months: float
    cash_on_hand: int
    monthly_burn: int
    scenario: str
    last_updated: str
    trends: Dict[str, float]

class FinancialTransaction(BaseModel):
    id: str
    type: str
    amount: int
    currency: str
    description: str
    category: str
    timestamp: str
    status: str
    merchant: str

class FinancialSummary(BaseModel):
    total_revenue: int
    total_expenses: int
    net_cash_flow: int
    transaction_count: int

class FinancialScenario(BaseModel):
    id: str
    name: str
    description: str
    runway_months: float
    cash_on_hand: int
    monthly_burn: int
    status: str

# Mock Financial Data
MOCK_SCENARIOS = {
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

MOCK_TRANSACTIONS = [
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
]

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Runway Navigator Financial API",
        "version": "1.0.0",
        "description": "Simple financial API for hackathon demo",
        "endpoints": {
            "health": "/health",
            "financial_kpis": "/financial/kpis",
            "financial_transactions": "/financial/transactions",
            "financial_scenarios": "/financial/scenarios",
            "financial_scenario_switch": "/financial/scenario/{scenario_id}"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0.0"
    }

@app.get("/financial/kpis")
async def get_financial_kpis():
    """Get real-time financial KPIs for dashboard"""
    # Get current scenario (default to healthy_saas)
    current_scenario = "healthy_saas"
    scenario_data = MOCK_SCENARIOS[current_scenario]
    
    return {
        "runway_months": scenario_data["runway_months"],
        "cash_on_hand": scenario_data["cash_on_hand"],
        "monthly_burn": scenario_data["monthly_burn"],
        "scenario": current_scenario,
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
    return {
        "transactions": MOCK_TRANSACTIONS,
        "summary": {
            "total_revenue": 225000,
            "total_expenses": 155000,
            "net_cash_flow": 70000,
            "transaction_count": len(MOCK_TRANSACTIONS)
        }
    }

@app.get("/financial/scenarios")
async def get_financial_scenarios():
    """Get available financial scenarios for demo"""
    scenarios = []
    for scenario_id, data in MOCK_SCENARIOS.items():
        scenarios.append({
            "id": scenario_id,
            "name": scenario_id.replace("_", " ").title(),
            "description": data["description"],
            "runway_months": data["runway_months"],
            "cash_on_hand": data["cash_on_hand"],
            "monthly_burn": data["monthly_burn"],
            "status": "active" if scenario_id == "healthy_saas" else "available"
        })
    
    return {"scenarios": scenarios}

@app.post("/financial/scenario/{scenario_id}")
async def switch_financial_scenario(scenario_id: str):
    """Switch to a different financial scenario for demo"""
    if scenario_id not in MOCK_SCENARIOS:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return {
        "message": f"Switched to {scenario_id} scenario",
        "scenario": MOCK_SCENARIOS[scenario_id],
        "timestamp": datetime.now().isoformat()
    }

# WebSocket for real-time financial updates
@app.websocket("/ws/financial")
async def financial_websocket(websocket):
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
            
            await websocket.send_text(str(mock_update))
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Runway Navigator Financial API...")
    print("📍 API will be available at: http://localhost:8001")
    print("📚 API documentation at: http://localhost:8001/docs")
    print("🔌 WebSocket at: ws://localhost:8001/ws/financial")
    
    uvicorn.run(
        "simple_financial_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
