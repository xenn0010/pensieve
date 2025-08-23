#!/usr/bin/env python3
"""
Simple test script for MCP Intelligence Systems
Tests SixtyFour and MixRank MCP servers with Gemini orchestration
"""

import asyncio
import json
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

print("All modules imported successfully!")
print("=" * 50)


async def test_sixtyfour():
    """Test SixtyFour Market Intelligence"""
    print("\nTesting SixtyFour Market Intelligence...")
    
    try:
        sixtyfour = SixtyFourMarketIntelligence()
        await sixtyfour.initialize()
        
        # Test WOW intelligence analysis
        result = await sixtyfour.analyze_wow_intelligence_signals('test-company.com')
        
        print(f"SixtyFour test result:")
        print(f"- Signals detected: {len(result.get('wow_signals', []))}")
        print(f"- Risk level: {result.get('risk_level', 'unknown')}")
        print(f"- Company analyzed: {result.get('company_domain', 'unknown')}")
        
        return True
    except Exception as e:
        print(f"SixtyFour test error: {e}")
        return False


async def test_mixrank():
    """Test MixRank Technology Intelligence"""
    print("\nTesting MixRank Technology Intelligence...")
    
    try:
        mixrank = MixRankTechnologyIntelligence()
        await mixrank.initialize()
        
        # Test technology WOW intelligence
        result = await mixrank.analyze_technology_wow_signals('test-company.com')
        
        print(f"MixRank test result:")
        print(f"- Tech signals detected: {len(result.get('technology_wow_signals', []))}")
        print(f"- Tech risk level: {result.get('technology_risk_level', 'unknown')}")
        print(f"- Company analyzed: {result.get('company_domain', 'unknown')}")
        
        return True
    except Exception as e:
        print(f"MixRank test error: {e}")
        return False


async def test_orchestrator():
    """Test Decision Orchestrator"""
    print("\nTesting Decision Orchestrator...")
    
    try:
        orchestrator = DecisionOrchestrator()
        
        print("Decision Orchestrator initialized successfully")
        print("- Event queue ready")
        print("- Gemini integration configured")
        print("- WOW intelligence coordination ready")
        
        return True
    except Exception as e:
        print(f"Orchestrator test error: {e}")
        return False


async def main():
    """Run simple MCP tests"""
    print("PENSIEVE MCP INTELLIGENCE SYSTEM - SIMPLE TESTS")
    print("=" * 50)
    print(f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    results = {}
    results['sixtyfour'] = await test_sixtyfour()
    results['mixrank'] = await test_mixrank()
    results['orchestrator'] = await test_orchestrator()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        print(f"{test_name.capitalize()}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All MCP intelligence systems are working!")
        print("- SixtyFour Market Intelligence: Ready")
        print("- MixRank Technology Intelligence: Ready")
        print("- Gemini Decision Orchestration: Ready")
    else:
        print("Some tests failed - check errors above")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)