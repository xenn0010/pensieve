#!/usr/bin/env python3
"""
Simple test for the SixtyFour API client
"""

import os
import sys
from unittest.mock import patch, MagicMock

# Add the specific directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp-servers', 'sixtyfour-mcp'))

try:
    from sixtyfour_api_client import enrich_lead, SixtyFourAPIError
    print("✅ Successfully imported sixtyfour_api_client")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)


def test_mock_api_call():
    """Test the client with mocked HTTP response"""
    print("\n=== Testing with Mock API Response ===")
    
    with patch.dict(os.environ, {'SIXTYFOUR_API_KEY': 'test-key-123'}):
        with patch('sixtyfour_api_client.requests.post') as mock_post:
            # Mock successful response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'structured_data': {
                    'company': 'Test Corp',
                    'intelligence': {
                        'risk_score': 0.3,
                        'insights': ['Low risk company', 'Stable growth']
                    }
                }
            }
            mock_post.return_value = mock_response
            
            lead_info = {'company': 'Test Corp', 'research_depth': 'basic'}
            struct = {'risk_assessment': 'analyze company risk'}
            
            try:
                result = enrich_lead(lead_info, struct)
                print("✅ Mock API call successful!")
                print(f"   Result: {result}")
                
                # Verify the mock was called
                mock_post.assert_called_once()
                print("✅ HTTP request was made correctly")
                
                return True
                
            except Exception as e:
                print(f"❌ Mock test failed: {e}")
                return False


def test_real_api_call():
    """Test with real API if key is available"""
    print("\n=== Testing with Real API ===")
    
    # Check for real API key
    api_key = os.getenv('SIXTYFOUR_API_KEY')
    if not api_key or 'test' in api_key.lower():
        print("⚠️  No real API key found, skipping real API test")
        print("   Set SIXTYFOUR_API_KEY environment variable to test real API")
        return True
    
    try:
        lead_info = {
            'company': 'openai',
            'research_depth': 'basic',
            'intelligence_type': 'competitive'
        }
        
        struct = {
            'financial_health': 'basic financial health indicators',
            'competitive_signals': 'competitive intelligence data'
        }
        
        print("🔄 Making real API call...")
        result = enrich_lead(lead_info, struct)
        
        print("✅ Real API call successful!")
        print(f"   Result type: {type(result)}")
        
        if isinstance(result, dict):
            print(f"   Keys: {list(result.keys())}")
            # Show first 300 chars of result
            result_str = str(result)
            if len(result_str) > 300:
                result_str = result_str[:300] + "..."
            print(f"   Data: {result_str}")
        
        return True
        
    except SixtyFourAPIError as e:
        print(f"❌ API error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False


def main():
    """Run all tests"""
    print("🧪 Testing SixtyFour API Client")
    
    success = True
    
    # Test 1: Mock API call
    if not test_mock_api_call():
        success = False
    
    # Test 2: Real API call (if key available)
    if not test_real_api_call():
        success = False
    
    print(f"\n{'🎉 All tests passed!' if success else '💥 Some tests failed!'}")
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
