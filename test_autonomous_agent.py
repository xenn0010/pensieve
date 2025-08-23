#!/usr/bin/env python3
"""
Test Suite for Pensieve Autonomous AI Agent
Tests end-to-end autonomous decision making and action execution
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Fix import path for intelligence-engine directory with hyphens
sys.path.insert(0, str(project_root / "intelligence-engine"))
from decision_orchestrator import DecisionOrchestrator, IntelligenceEvent, EventType, Priority
from autonomous_action_engine import AutonomousActionEngine
from config.settings import settings
import json
from datetime import datetime

async def test_intelligence_data_fetching():
    """Test MCP server data fetching capabilities"""
    print("\n=== Testing Intelligence Data Fetching ===")
    
    # Add MCP servers to path
    mcp_servers_path = project_root / "mcp-servers"
    sys.path.insert(0, str(mcp_servers_path / "sixtyfour-mcp"))
    sys.path.insert(0, str(mcp_servers_path / "mixrank-mcp"))
    
    try:
        from market_intelligence import SixtyFourMarketIntelligence
        from technology_intelligence import MixRankTechnologyIntelligence
        
        # Test SixtyFour intelligence
        print("Testing SixtyFour market intelligence...")
        sixtyfour = SixtyFourMarketIntelligence()
        
        # Test company enrichment
        test_company = "anthropic.com"
        market_data = await sixtyfour.enrich_company(test_company)
        print(f"SixtyFour data for {test_company}: {json.dumps(market_data, indent=2)}")
        
        # Test MixRank intelligence
        print("\nTesting MixRank technology intelligence...")
        mixrank = MixRankTechnologyIntelligence()
        
        # Test company matching
        company_match = await mixrank.get_company_match(test_company)
        print(f"MixRank company match: {json.dumps(company_match, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"Intelligence fetching failed: {e}")
        return False

async def test_decision_orchestrator():
    """Test Gemini AI decision orchestration"""
    print("\n=== Testing Gemini Decision Orchestrator ===")
    
    try:
        orchestrator = DecisionOrchestrator()
        
        # Create test intelligence event
        test_event = IntelligenceEvent(
            event_type=EventType.COMPETITOR_DISTRESS,
            priority=Priority.HIGH,
            data={
                "company": "competitor-xyz.com",
                "signal_type": "digital_exodus",
                "confidence": 0.87,
                "predicted_layoffs": 200,
                "timeline": "30 days",
                "opportunity_value": 2300000
            },
            source="sixtyfour",
            timestamp=datetime.now()
        )
        
        print(f"Processing intelligence event: {test_event.event_type}")
        
        # Process event through orchestrator
        decision = await orchestrator.process_intelligence_event(test_event)
        
        print(f"Gemini decision: {json.dumps(decision, indent=2, default=str)}")
        
        return decision
        
    except Exception as e:
        print(f"Decision orchestration failed: {e}")
        return None

async def test_autonomous_actions(decision_data):
    """Test autonomous action execution"""
    print("\n=== Testing Autonomous Action Execution ===")
    
    try:
        action_engine = AutonomousActionEngine()
        
        if not decision_data or 'recommended_actions' not in decision_data:
            print("No recommended actions from decision orchestrator")
            return False
        
        # Execute recommended actions
        results = []
        for action in decision_data['recommended_actions']:
            print(f"Executing action: {action['action_type']}")
            
            result = await action_engine.execute_action(
                action_type=action['action_type'],
                parameters=action.get('parameters', {}),
                confidence_score=action.get('confidence', 0.8)
            )
            
            results.append(result)
            print(f"Action result: {result.status} - {result.message}")
            
            if result.business_impact:
                print(f"Business impact: {json.dumps(result.business_impact, indent=2)}")
        
        return len([r for r in results if r.success]) > 0
        
    except Exception as e:
        print(f"Autonomous action execution failed: {e}")
        return False

async def test_end_to_end_scenario():
    """Test complete end-to-end autonomous agent scenario"""
    print("\n=== End-to-End Autonomous Agent Test ===")
    
    try:
        # Initialize components
        orchestrator = DecisionOrchestrator()
        action_engine = AutonomousActionEngine()
        
        # Simulate customer churn scenario
        churn_event = IntelligenceEvent(
            event_type=EventType.CUSTOMER_CHURN_RISK,
            priority=Priority.HIGH,
            data={
                "customer_id": "enterprise_client_001",
                "customer_name": "TechCorp Industries",
                "churn_probability": 0.92,
                "contract_value": 850000,
                "risk_factors": ["decreased_usage", "support_tickets_spike", "contract_renewal_delay"],
                "timeline": "15 days"
            },
            source="pylon",
            timestamp=datetime.now()
        )
        
        print("Simulating high-value customer churn risk scenario...")
        print(f"Customer: {churn_event.data['customer_name']}")
        print(f"Churn probability: {churn_event.data['churn_probability'] * 100}%")
        print(f"At-risk revenue: ${churn_event.data['contract_value']:,}")
        
        # Process through decision orchestrator
        decision = await orchestrator.process_intelligence_event(churn_event)
        
        if decision and decision.get('execution_mode') == 'autonomous':
            print(f"Confidence: {decision['confidence_score']} - AUTONOMOUS EXECUTION")
            
            # Execute actions automatically
            for action in decision['recommended_actions']:
                result = await action_engine.execute_action(
                    action_type=action['action_type'],
                    parameters=action.get('parameters', {}),
                    confidence_score=decision['confidence_score']
                )
                
                print(f"AUTO-EXECUTED: {action['action_type']} - {result.status}")
                if result.business_impact:
                    print(f"Impact: {result.business_impact}")
        
        return True
        
    except Exception as e:
        print(f"End-to-end test failed: {e}")
        return False

async def main():
    """Run comprehensive autonomous agent tests"""
    print("PENSIEVE AUTONOMOUS AGENT TEST SUITE")
    print("=" * 50)
    
    # Test 1: Intelligence data fetching
    intelligence_success = await test_intelligence_data_fetching()
    
    # Test 2: Decision orchestration
    decision_result = await test_decision_orchestrator()
    
    # Test 3: Autonomous actions
    action_success = await test_autonomous_actions(decision_result)
    
    # Test 4: End-to-end scenario
    e2e_success = await test_end_to_end_scenario()
    
    # Results summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Intelligence Fetching: {'✓ PASS' if intelligence_success else '✗ FAIL'}")
    print(f"Decision Orchestration: {'✓ PASS' if decision_result else '✗ FAIL'}")
    print(f"Autonomous Actions: {'✓ PASS' if action_success else '✗ FAIL'}")
    print(f"End-to-End Scenario: {'✓ PASS' if e2e_success else '✗ FAIL'}")
    
    overall_success = intelligence_success and decision_result and action_success and e2e_success
    print(f"\nOVERALL SYSTEM STATUS: {'OPERATIONAL' if overall_success else 'ISSUES DETECTED'}")
    
    return overall_success

if __name__ == "__main__":
    asyncio.run(main())