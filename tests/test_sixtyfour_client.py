#!/usr/bin/env python3
"""
Test the refactored SixtyFour API client
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

# Import the client directly
from mcp_servers.sixtyfour_mcp.sixtyfour_api_client import enrich_lead, SixtyFourAPIError


class TestSixtyFourAPIClient(unittest.TestCase):
    
    def setUp(self):
        # Mock API key
        self.api_key_patcher = patch.dict(os.environ, {'SIXTYFOUR_API_KEY': 'test-key-123'})
        self.api_key_patcher.start()
    
    def tearDown(self):
        self.api_key_patcher.stop()
    
    @patch('mcp_servers.sixtyfour_mcp.sixtyfour_api_client.requests.post')
    def test_successful_api_call(self, mock_post):
        """Test successful API call returns structured data"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'structured_data': {
                'company': 'Test Corp',
                'intelligence': {'risk_score': 0.3}
            }
        }
        mock_post.return_value = mock_response
        
        lead_info = {'company': 'Test Corp', 'research_depth': 'basic'}
        struct = {'risk_assessment': 'analyze company risk'}
        
        result = enrich_lead(lead_info, struct)
        
        # Verify API was called correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        self.assertEqual(call_args[1]['json']['lead_info'], lead_info)
        self.assertEqual(call_args[1]['json']['struct'], struct)
        self.assertIn('x-api-key', call_args[1]['headers'])
        self.assertEqual(call_args[1]['headers']['x-api-key'], 'test-key-123')
        
        # Verify result
        self.assertEqual(result['company'], 'Test Corp')
        self.assertEqual(result['intelligence']['risk_score'], 0.3)
    
    @patch('mcp_servers.sixtyfour_mcp.sixtyfour_api_client.requests.post')
    def test_api_error_response(self, mock_post):
        """Test API error response raises SixtyFourAPIError"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = 'Bad request'
        mock_post.return_value = mock_response
        
        lead_info = {'company': 'Test Corp'}
        struct = {'risk_assessment': 'analyze'}
        
        with self.assertRaises(SixtyFourAPIError):
            enrich_lead(lead_info, struct)
    
    def test_missing_api_key(self):
        """Test missing API key raises error"""
        # Remove API key from environment
        with patch.dict(os.environ, {}, clear=True):
            with patch('mcp_servers.sixtyfour_mcp.sixtyfour_api_client.settings') as mock_settings:
                mock_settings.sixtyfour_api_key = None
                
                with self.assertRaises(SixtyFourAPIError) as cm:
                    enrich_lead({'company': 'Test'}, {})
                
                self.assertIn('API key not configured', str(cm.exception))


def test_integration():
    """Simple integration test (requires real API key)"""
    print("\n=== SixtyFour Client Integration Test ===")
    
    # Check if we have a real API key
    api_key = os.getenv('SIXTYFOUR_API_KEY')
    if not api_key or api_key == 'test-key-123':
        print("⚠️  No real API key found, skipping integration test")
        print("   Set SIXTYFOUR_API_KEY environment variable to run integration test")
        return True
    
    try:
        lead_info = {
            'company': 'openai',
            'research_depth': 'basic',
            'intelligence_type': 'competitive'
        }
        
        struct = {
            'financial_health': 'basic financial indicators',
            'competitive_position': 'market position analysis'
        }
        
        print("🔄 Calling SixtyFour API...")
        result = enrich_lead(lead_info, struct)
        
        print("✅ API call successful!")
        print(f"   Result type: {type(result)}")
        print(f"   Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict) and result:
            print(f"   Sample data: {str(result)[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False


if __name__ == '__main__':
    print("Running SixtyFour API client tests...")
    
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
    
    # Run integration test
    success = test_integration()
    
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed'}")
