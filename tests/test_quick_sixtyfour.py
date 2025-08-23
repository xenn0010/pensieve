#!/usr/bin/env python3
"""
Quick test with real SixtyFour API - lighter requests
"""

import os
import sys
import json

# Add the specific directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp-servers', 'sixtyfour-mcp'))

from sixtyfour_api_client import enrich_lead, SixtyFourAPIError

def test_lightweight_request():
    """Test with a lightweight request that should respond quickly"""
    print("🚀 Testing lightweight SixtyFour API request")
    
    # Set API key
    os.environ['SIXTYFOUR_API_KEY'] = "yj9TfC1UL5MFUpVmjjpb4rCtErtoPaYk"
    
    # Simple, fast request
    lead_info = {
        "company": "stripe",
        "research_depth": "basic"  # Basic instead of maximum
    }
    
    # Minimal struct for faster response
    struct = {
        "company_overview": "basic company information",
        "financial_status": "high-level financial indicators"
    }
    
    try:
        print(f"📡 Calling API for {lead_info['company']} with basic research...")
        result = enrich_lead(lead_info, struct)
        
        print("✅ SUCCESS! API call completed")
        print(f"📊 Response type: {type(result)}")
        
        if isinstance(result, dict):
            print(f"🔑 Keys: {list(result.keys())}")
            
            # Show the data
            print("\n📄 Response Data:")
            print("-" * 40)
            if result:
                for key, value in result.items():
                    print(f"{key}: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}")
            else:
                print("(Empty response)")
            print("-" * 40)
        
        return True
        
    except SixtyFourAPIError as e:
        print(f"❌ API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_another_company():
    """Test with another company to verify consistency"""
    print("\n🏢 Testing another company...")
    
    lead_info = {
        "company": "github", 
        "research_depth": "basic"
    }
    
    struct = {
        "market_position": "current market standing",
        "growth_signals": "business growth indicators"
    }
    
    try:
        result = enrich_lead(lead_info, struct)
        print(f"✅ Second test successful! Keys: {list(result.keys()) if isinstance(result, dict) else 'No dict'}")
        return True
    except Exception as e:
        print(f"❌ Second test failed: {e}")
        return False

if __name__ == '__main__':
    print("⚡ Quick SixtyFour API Test")
    print("=" * 30)
    
    test1 = test_lightweight_request()
    test2 = test_another_company()
    
    if test1 or test2:
        print(f"\n🎉 Real API working! (test1: {test1}, test2: {test2})")
    else:
        print("\n💥 All tests failed")
        
    print("\n✨ Test completed!")
