#!/usr/bin/env python3
"""
Test real SixtyFour API call - exactly like the Colab notebook
"""

import os
import sys
import json

# Add the specific directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp-servers', 'sixtyfour-mcp'))

try:
    from sixtyfour_api_client import enrich_lead, SixtyFourAPIError
    print("✅ Successfully imported sixtyfour_api_client")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)


def test_real_api():
    """Test with real SixtyFour API - matching Colab notebook approach"""
    print("\n🔍 Testing Real SixtyFour API Call")
    
    # Set API key (you'll need to provide this)
    api_key = "yj9TfC1UL5MFUpVmjjpb4rCtErtoPaYk"  # Your actual API key from the notebook
    os.environ['SIXTYFOUR_API_KEY'] = api_key
    
    # Test data - using the same structure as your Colab notebook
    lead_info = {
        "company": "openai", 
        "research_depth": "maximum",
        "intelligence_type": "competitive"
    }
    
    struct = {
        "financial_health": "Analyze vendor payment patterns, hiring velocity, cash flow signals",
        "competitive_signals": "Talent poaching, customer migration, pricing intelligence", 
        "strategic_shifts": "Product pivot signals, market repositioning, technology adoption",
        "customer_intelligence": "Customer expansion patterns, integration depth, renewal risks",
        "market_opportunities": "Growth areas, acquisition opportunities, market gaps"
    }
    
    try:
        print(f"🔄 Making API call to SixtyFour for: {lead_info['company']}")
        print(f"📋 Research depth: {lead_info['research_depth']}")
        
        result = enrich_lead(lead_info, struct)
        
        print("✅ API Call Successful!")
        print(f"📊 Result type: {type(result)}")
        
        if isinstance(result, dict):
            print(f"🔑 Available keys: {list(result.keys())}")
            
            # Pretty print the result
            print("\n📄 Full Response:")
            print("=" * 50)
            print(json.dumps(result, indent=2)[:2000] + ("..." if len(str(result)) > 2000 else ""))
            print("=" * 50)
            
            # Extract specific insights if available
            if 'financial_health' in result:
                print(f"\n💰 Financial Health: {result['financial_health']}")
            
            if 'competitive_signals' in result:
                print(f"\n🎯 Competitive Signals: {result['competitive_signals']}")
                
            if 'market_opportunities' in result:
                print(f"\n🚀 Market Opportunities: {result['market_opportunities']}")
        
        return True
        
    except SixtyFourAPIError as e:
        print(f"❌ SixtyFour API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        print(f"📜 Full traceback:\n{traceback.format_exc()}")
        return False


def test_simple_company():
    """Test with a simpler company"""
    print("\n🏢 Testing with simpler company data")
    
    lead_info = {
        "company": "stripe",
        "research_depth": "basic"
    }
    
    struct = {
        "competitive_analysis": "basic competitive intelligence",
        "financial_signals": "basic financial health indicators"
    }
    
    try:
        result = enrich_lead(lead_info, struct)
        print("✅ Simple test successful!")
        print(f"📊 Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        return True
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return False


if __name__ == '__main__':
    print("🧪 Testing Real SixtyFour API Integration")
    print("=" * 60)
    
    success1 = test_real_api()
    success2 = test_simple_company()
    
    if success1 and success2:
        print("\n🎉 All real API tests passed!")
    else:
        print(f"\n💥 Some tests failed - success1: {success1}, success2: {success2}")
    
    print("\n✨ Test completed!")
