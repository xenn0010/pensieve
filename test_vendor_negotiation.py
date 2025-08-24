#!/usr/bin/env python3
"""
Test Autonomous Vendor Negotiation System
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "intelligence-engine"))

from autonomous_agent import PensieveAutonomousAgent, IntelligenceEvent, EventType, Priority
from datetime import datetime

async def test_vendor_negotiation():
    """Test autonomous vendor negotiation when company is losing money"""
    
    print("=== TESTING AUTONOMOUS VENDOR NEGOTIATION ===")
    print()
    
    # Initialize agent
    agent = PensieveAutonomousAgent()
    
    # Create financial crisis event that should trigger REAL vendor negotiations
    financial_crisis_event = IntelligenceEvent(
        event_type=EventType.FINANCIAL_CRISIS,
        priority=Priority.CRITICAL,
        data={
            "available_cash": 500000,
            "monthly_expenses": 200000,  # High burn rate
            "daily_burn": 6500,
            "runway_days": 77,  # Critical runway
            "cash_flow_pressure": 0.85,  # High pressure
            "financial_crisis": True,
            "vendors": ["aws.com", "salesforce.com", "slack.com"],
            "threat_timeline": "60 days"
        },
        source="brex",
        timestamp=datetime.now(),
        confidence=0.92
    )
    
    print("Financial Crisis Scenario:")
    print(f"- Cash available: ${financial_crisis_event.data['available_cash']:,}")
    print(f"- Monthly burn: ${financial_crisis_event.data['monthly_expenses']:,}")
    print(f"- Runway: {financial_crisis_event.data['runway_days']} days")
    print(f"- Cash flow pressure: {financial_crisis_event.data['cash_flow_pressure']:.0%}")
    print()
    
    # Process the event - should trigger REAL vendor negotiations
    print("Processing financial crisis event...")
    results = await agent.process_intelligence_event(financial_crisis_event)
    
    print(f"\nActions Executed: {len(results)}")
    print("=" * 50)
    
    # Look for vendor negotiation results
    for result in results:
        print(f"\nAction: {result.action_type}")
        print(f"Status: {'SUCCESS' if result.success else 'FAILED'}")
        print(f"Message: {result.message}")
        
        if result.business_impact:
            impact = result.business_impact
            
            # Check if this is the real vendor negotiation
            if impact.get("negotiation_type") == "REAL_AUTONOMOUS":
                print("\nREAL AUTONOMOUS VENDOR NEGOTIATIONS DETECTED!")
                print("-" * 50)
                print(f"Vendors contacted: {impact['vendors_contacted']}")
                print(f"Negotiations initiated: {impact['negotiations_initiated']}")
                print(f"Expected savings: ${impact['expected_savings']:,.2f}")
                print(f"Contact method: {impact['contact_method']}")
                print()
                
                if 'negotiation_details' in impact:
                    print("Negotiation Details:")
                    for detail in impact['negotiation_details']:
                        print(f"  • {detail['vendor']}: {detail['negotiation_status']}")
                        print(f"    Expected savings: ${detail['expected_savings']:,.2f}")
                
                print("\nREAL EMAIL NEGOTIATIONS HAVE BEEN INITIATED")
                print("   Vendors will receive professional negotiation emails")
                print("   within the next few minutes.")
            
            elif result.action_type == "vendor_contract_renegotiation":
                print(f"\nBusiness Impact: {impact}")
        
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Cost: ${result.cost:.2f}")

    print("\n" + "=" * 50)
    print("VENDOR NEGOTIATION TEST COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_vendor_negotiation())