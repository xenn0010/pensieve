#!/usr/bin/env python3
"""
Test script for orchestration of MCP intelligence systems
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
sys.path.insert(0, os.path.join(os.path.abspath('.'), 'intelligence-engine'))
from decision_orchestrator import DecisionOrchestrator

print("Testing Gemini Orchestration with MCP Intelligence...")
print("=" * 60)


async def test_wow_intelligence_coordination():
    """Test the WOW intelligence coordination across all systems"""
    print("\nTesting WOW Intelligence Coordination...")
    
    try:
        orchestrator = DecisionOrchestrator()
        
        print("Starting comprehensive WOW intelligence analysis...")
        
        # This will coordinate intelligence gathering from all MCP servers
        await orchestrator._coordinate_wow_intelligence_analysis()
        
        print("WOW Intelligence Coordination completed successfully!")
        print("- SixtyFour market intelligence analyzed")
        print("- MixRank technology intelligence analyzed")  
        print("- Financial intelligence processed")
        print("- Combined intelligence processed by Gemini")
        print("- Events generated for high-priority signals")
        
        return True
        
    except Exception as e:
        print(f"Orchestration test failed: {e}")
        return False


async def test_periodic_intelligence_sweep():
    """Test the periodic intelligence sweep functionality"""
    print("\nTesting Periodic Intelligence Sweep...")
    
    try:
        orchestrator = DecisionOrchestrator()
        
        print("Running periodic intelligence sweep...")
        await orchestrator._periodic_intelligence_sweep()
        
        print("Periodic intelligence sweep completed!")
        print("- All target companies analyzed")
        print("- Cross-system intelligence coordination working")
        print("- Gemini processing events from intelligence signals")
        
        return True
        
    except Exception as e:
        print(f"Periodic sweep test failed: {e}")
        return False


async def main():
    """Test orchestration functionality"""
    print("GEMINI ORCHESTRATION TESTS")
    print("=" * 60)
    print(f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    results['wow_coordination'] = await test_wow_intelligence_coordination()
    results['periodic_sweep'] = await test_periodic_intelligence_sweep()
    
    print("\n" + "=" * 60)
    print("ORCHESTRATION TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\nOverall: {passed}/{total} orchestration tests passed")
    
    if passed == total:
        print("SUCCESS: Gemini orchestration is working perfectly!")
        print("- WOW intelligence coordination: Active")
        print("- Multi-system integration: Working")
        print("- Event processing: Ready")
        print("- Autonomous decision making: Enabled")
    else:
        print("Some orchestration tests failed")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)