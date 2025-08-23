#!/usr/bin/env python3
"""
Test real company analysis with MCP servers and Gemini
"""

import asyncio
import sys
import os
from datetime import datetime

# Add paths for imports
sys.path.insert(0, os.path.abspath('.'))
mcp_servers_path = os.path.join(os.path.abspath('.'), 'mcp-servers')
sys.path.insert(0, mcp_servers_path)

# Import modules
sys.path.insert(0, os.path.join(mcp_servers_path, 'sixtyfour-mcp'))
from market_intelligence import SixtyFourMarketIntelligence

sys.path.insert(0, os.path.join(mcp_servers_path, 'mixrank-mcp'))
from technology_intelligence import MixRankTechnologyIntelligence

sys.path.insert(0, os.path.join(os.path.abspath('.'), 'intelligence-engine'))
from decision_orchestrator import DecisionOrchestrator


async def test_real_company_analysis():
    """Test real company analysis with Gemini orchestration"""
    
    # Real company to analyze
    target_company = "openai.com"
    
    print(f"Analyzing real company: {target_company}")
    print("=" * 50)
    
    # Initialize systems
    orchestrator = DecisionOrchestrator()
    sixtyfour = SixtyFourMarketIntelligence()
    mixrank = MixRankTechnologyIntelligence()
    
    await sixtyfour.initialize()
    await mixrank.initialize()
    
    # Step 1: Get SixtyFour market intelligence
    print("Step 1: Fetching SixtyFour market intelligence...")
    market_intel = await sixtyfour.analyze_wow_intelligence_signals(target_company)
    
    # Step 2: Get MixRank technology intelligence  
    print("Step 2: Fetching MixRank technology intelligence...")
    tech_intel = await mixrank.analyze_technology_wow_signals(target_company)
    
    # Step 3: Combine intelligence data
    print("Step 3: Combining intelligence data...")
    combined_intelligence = {
        'sixtyfour_intelligence': market_intel,
        'mixrank_intelligence': tech_intel,
        'analysis_timestamp': datetime.now().isoformat()
    }
    
    # Step 4: Process with Gemini orchestrator
    print("Step 4: Processing with Gemini orchestrator...")
    await orchestrator._process_combined_intelligence(target_company, combined_intelligence)
    
    # Display results
    print("\nANALYSIS RESULTS")
    print("=" * 50)
    
    # Market intelligence results
    market_signals = market_intel.get('wow_signals', [])
    print(f"Market Intelligence: {len(market_signals)} signals detected")
    for i, signal in enumerate(market_signals[:3], 1):
        print(f"  {i}. {signal.get('signal_type', 'Unknown')} - Severity: {signal.get('severity', 'medium')}")
    
    # Technology intelligence results  
    tech_signals = tech_intel.get('technology_wow_signals', [])
    print(f"Technology Intelligence: {len(tech_signals)} tech signals detected")
    for i, signal in enumerate(tech_signals[:3], 1):
        print(f"  {i}. {signal.get('signal_type', 'Unknown')} - Severity: {signal.get('severity', 'medium')}")
    
    # Risk assessment
    print(f"Market Risk Level: {market_intel.get('risk_level', 'unknown')}")
    print(f"Technology Risk Level: {tech_intel.get('technology_risk_level', 'unknown')}")
    
    # Top recommendations
    all_actions = []
    all_actions.extend(market_intel.get('recommended_actions', [])[:2])
    all_actions.extend(tech_intel.get('recommended_technology_actions', [])[:2])
    
    if all_actions:
        print("Top Recommendations:")
        for i, action in enumerate(all_actions[:3], 1):
            print(f"  {i}. {action}")
    
    print(f"\nAnalysis completed for {target_company}")
    return True


async def main():
    """Run real company analysis test"""
    print("REAL COMPANY ANALYSIS WITH GEMINI MCP ORCHESTRATION")
    print("=" * 60)
    print(f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        success = await test_real_company_analysis()
        
        if success:
            print("\nSUCCESS: Real company analysis completed")
            print("- SixtyFour data fetched and analyzed")
            print("- MixRank data fetched and analyzed") 
            print("- Gemini orchestration processed results")
            print("- Intelligence signals detected and processed")
        
        return success
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)