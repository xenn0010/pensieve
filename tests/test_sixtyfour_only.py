#!/usr/bin/env python3
"""
Simple SixtyFour API test
"""

import asyncio
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.abspath('.'))
mcp_servers_path = os.path.join(os.path.abspath('.'), 'mcp-servers')
sys.path.insert(0, mcp_servers_path)

# Import modules
sys.path.insert(0, os.path.join(mcp_servers_path, 'sixtyfour-mcp'))
from market_intelligence import SixtyFourMarketIntelligence

async def test_sixtyfour_api():
    """Test SixtyFour API directly"""
    print("Testing SixtyFour API...")
    
    try:
        sixtyfour = SixtyFourMarketIntelligence()
        await sixtyfour.initialize()
        
        # Test with a simple company
        result = await sixtyfour.analyze_wow_intelligence_signals('openai.com')
        
        print("SixtyFour test completed")
        print(f"Result: {type(result)}")
        print(f"Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        return True
        
    except Exception as e:
        print(f"SixtyFour test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_sixtyfour_api())
    exit(0 if success else 1)