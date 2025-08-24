from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
from datetime import datetime

# Assuming CFOFinancialMethods and MockFinancialDataGenerator are available
# We'll need to adjust the import path based on the final structure
from mcp_servers.brex_mcp.financial_monitor import CFOFinancialMethods
from mcp_servers.brex_mcp.mock_financial_data import MockFinancialDataGenerator

# Placeholder for OpenAI integration
class OpenAIService:
    async def analyze_cfo_results(self, method_name: str, results: Dict[str, Any]) -> Dict[str, Any]:
        # In a real scenario, this would call the OpenAI API
        # and send the method_name and results for analysis.
        # For now, we'll return a mock analysis.
        logging.info(f"Sending {method_name} results to OpenAI for analysis.")
        mock_analysis = {
            "summary": f"AI analysis for {method_name}: The financial data indicates a {results.get('overall_status', 'neutral')} trend.",
            "recommendations": [
                "Review key metrics closely for the next quarter.",
                "Consider adjusting budgets based on variances."
            ],
            "confidence": 0.85,
            "ai_model": "gpt-5 (mock)",
            "analysis_timestamp": datetime.now().isoformat()
        }
        return mock_analysis


app = FastAPI(
    title="CFO Financial Analysis API",
    description="API for performing CFO financial methods and AI analysis."
)

# Initialize mock data generator and CFO methods
mock_generator = MockFinancialDataGenerator() # Using default profile for now
cfo_methods = CFOFinancialMethods(mock_generator)
openai_service = OpenAIService()


class CashFlowForecastInput(BaseModel):
    periods: int = 12


class BudgetVarianceAnalysisInput(BaseModel):
    budget_data: Dict[str, float]
    actual_data: Dict[str, float]


@app.post("/cfo/cash-flow-forecast", response_model=Dict[str, Any])
async def cash_flow_forecast(input: CashFlowForecastInput):
    """
    Performs cash flow forecasting and provides AI-driven analysis.
    """
    try:
        forecast_results = await cfo_methods.cash_flow_forecasting(periods=input.periods)
        ai_analysis = await openai_service.analyze_cfo_results("Cash Flow Forecasting", forecast_results)
        return {"forecast_results": forecast_results, "ai_analysis": ai_analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cfo/budget-variance-analysis", response_model=Dict[str, Any])
async def budget_variance_analysis(input: BudgetVarianceAnalysisInput):
    """
    Performs budget variance analysis and provides AI-driven analysis.
    """
    try:
        variance_results = await cfo_methods.budget_variance_analysis(
            budget_data=input.budget_data,
            actual_data=input.actual_data
        )
        ai_analysis = await openai_service.analyze_cfo_results("Budget Variance Analysis", variance_results)
        return {"variance_results": variance_results, "ai_analysis": ai_analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
