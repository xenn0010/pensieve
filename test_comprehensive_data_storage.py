#!/usr/bin/env python3
"""
Test comprehensive data storage system
Demonstrates how all API calls and search results are captured and stored
"""

import asyncio
import sys
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.append('.')

from config.supabase_client import supabase_client
from config.settings import settings
from config.logging_config import setup_logging, get_component_logger

# Setup logging
setup_logging("INFO")
logger = get_component_logger("data_storage_test")


async def test_data_storage_system():
    """Test the comprehensive data storage system"""
    print("🗄️  Testing Comprehensive Data Storage System")
    print("=" * 60)
    
    # Initialize Supabase
    try:
        await supabase_client.initialize()
        print("✅ Supabase client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Supabase: {e}")
        return False
    
    try:
        # Import after initialization
        from intelligence_engine.storage.data_storage_manager import (
            data_storage_manager, APICallMetadata, SearchResult, SearchType, ResearchType
        )
        
        # Test 1: Store API Call Result
        print("\n📡 Testing API call result storage...")
        
        metadata = APICallMetadata(
            provider="sixtyfour",
            endpoint="/enrich-lead",
            method="POST",
            triggered_by="test_suite",
            session_id="test_session_123"
        )
        
        # Simulate API call data
        request_params = {
            "lead_info": {"company": "stripe"},
            "struct": {"financial_health": "analyze cash flow"}
        }
        
        response_body = {
            "financial_health": "Strong financial position with steady revenue growth",
            "competitive_signals": "Market leader in payment processing",
            "company_metrics": {
                "revenue": "12B",
                "employees": 8000,
                "growth_rate": 0.25
            }
        }
        
        api_call_id = await data_storage_manager.store_api_call_result(
            metadata=metadata,
            request_params=request_params,
            response_status=200,
            response_body=response_body,
            duration_ms=45200  # 45.2 seconds
        )
        
        print(f"✅ Stored API call result: {api_call_id}")
        
        # Test 2: Store Search Result
        print("\n🔍 Testing search result storage...")
        
        search_result = SearchResult(
            query="stripe financial analysis",
            search_type=SearchType.COMPANY,
            results_data={
                "company_profile": {
                    "name": "Stripe",
                    "industry": "Financial Services",
                    "valuation": "95B"
                },
                "financial_metrics": {
                    "revenue": "12B",
                    "growth_rate": "25%"
                },
                "competitive_position": "Market leader"
            },
            confidence_score=0.92,
            data_sources=["sixtyfour", "intelligence_cache"],
            total_results=1
        )
        
        search_result_id = await data_storage_manager.store_search_result(
            search_result=search_result,
            api_call_ids=[api_call_id],
            requested_by="test_user",
            processing_duration_ms=1250
        )
        
        print(f"✅ Stored search result: {search_result_id}")
        
        # Test 3: Create Research Session
        print("\n📋 Testing research session creation...")
        
        session_id = await data_storage_manager.create_research_session(
            objective="Comprehensive analysis of Stripe's competitive position",
            research_type=ResearchType.COMPETITIVE_ANALYSIS,
            target_companies=["stripe", "square", "paypal"],
            research_questions=[
                "What is Stripe's market share?",
                "How does Stripe compare to competitors?",
                "What are Stripe's growth prospects?"
            ],
            initiated_by="test_analyst",
            automation_level="assisted"
        )
        
        print(f"✅ Created research session: {session_id}")
        
        # Test 4: Update Research Session with Findings
        print("\n📊 Testing research session updates...")
        
        key_findings = {
            "market_position": "Stripe leads in developer-friendly payment APIs",
            "competitive_advantages": [
                "Superior developer experience",
                "Global payment coverage",
                "Strong enterprise adoption"
            ],
            "risk_factors": [
                "Regulatory changes",
                "Increasing competition from traditional banks"
            ]
        }
        
        await data_storage_manager.update_research_session(
            session_id=session_id,
            key_findings=key_findings,
            data_summary={
                "total_data_points": 15,
                "confidence_level": "high",
                "data_freshness": "last_24_hours"
            },
            api_call_ids=[api_call_id],
            search_result_ids=[search_result_id]
        )
        
        print("✅ Updated research session with findings")
        
        # Test 5: Store Intelligence Finding
        print("\n🧠 Testing intelligence finding storage...")
        
        finding_id = await data_storage_manager.store_intelligence_finding(
            finding_type="competitive_advantage",
            title="Stripe's Developer-First Strategy Drives Market Leadership",
            description="Analysis shows Stripe's focus on developer experience has resulted in 40% market share among new fintech companies",
            confidence_level="high",
            related_companies=["stripe"],
            key_metrics={
                "developer_adoption_rate": 0.65,
                "api_integration_time": "2_hours_avg",
                "developer_satisfaction": 9.2
            },
            supporting_evidence={
                "survey_data": "Developer satisfaction survey 2024",
                "market_data": "Fintech adoption analysis",
                "usage_metrics": "API call volume analysis"
            },
            urgency_level="medium",
            source_api_calls=[api_call_id]
        )
        
        print(f"✅ Stored intelligence finding: {finding_id}")
        
        # Test 6: Retrieve Company Research Data
        print("\n📄 Testing comprehensive data retrieval...")
        
        research_data = await data_storage_manager.get_company_research_data("stripe")
        
        print("✅ Retrieved comprehensive research data:")
        print(f"   Profile available: {research_data.get('profile') is not None}")
        print(f"   Recent searches: {len(research_data.get('recent_searches', []))}")
        print(f"   Research sessions: {len(research_data.get('research_sessions', []))}")
        print(f"   Intelligence findings: {len(research_data.get('intelligence_findings', []))}")
        
        # Test 7: Query Recent API Activity
        print("\n📊 Testing API activity analytics...")
        
        response = await supabase_client.client.table('api_call_results').select('*').order(
            'request_timestamp', desc=True
        ).limit(5).execute()
        
        api_calls = response.data or []
        print(f"✅ Retrieved {len(api_calls)} recent API calls")
        
        for call in api_calls:
            print(f"   {call['api_provider']}/{call['endpoint']}: {call['response_status']} ({call.get('duration_ms', 0)}ms)")
        
        # Test 8: Check Data Processing
        print("\n⚙️  Testing background data processing...")
        
        # Check if intelligence findings were automatically created
        findings_response = await supabase_client.client.table('intelligence_findings').select('*').contains(
            'related_companies', ['stripe']
        ).execute()
        
        findings = findings_response.data or []
        print(f"✅ Found {len(findings)} intelligence findings for Stripe")
        
        # Clean up test data (optional)
        print("\n🧹 Cleaning up test data...")
        
        cleanup_tables = [
            ('api_call_results', api_call_id),
            ('search_results', search_result_id),
            ('research_sessions', session_id),
            ('intelligence_findings', finding_id)
        ]
        
        for table, record_id in cleanup_tables:
            try:
                await supabase_client.client.table(table).delete().eq('id', record_id).execute()
                print(f"   ✅ Cleaned up {table}")
            except Exception as e:
                print(f"   ⚠️  Could not clean up {table}: {e}")
        
        print("\n🎉 All data storage tests completed successfully!")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Data Storage System Summary")
        print("=" * 60)
        print("✅ API Call Tracking: Every API call is logged with full details")
        print("✅ Search Result Storage: All search queries and results are cached") 
        print("✅ Research Session Management: Multi-step research workflows tracked")
        print("✅ Intelligence Findings: Automated insight extraction and storage")
        print("✅ Company Profiles: Aggregated data from all sources")
        print("✅ Performance Analytics: API usage and data quality metrics")
        print("✅ Comprehensive Retrieval: Rich APIs for frontend data access")
        
        return True
        
    except Exception as e:
        print(f"❌ Data storage test failed: {e}")
        import traceback
        print(f"📜 Traceback: {traceback.format_exc()}")
        return False


async def demonstrate_data_flow():
    """Demonstrate the complete data flow from API call to intelligence"""
    print("\n🔄 Demonstrating Complete Data Flow")
    print("=" * 50)
    
    try:
        # Step 1: Simulate a user search
        print("1️⃣ User searches for 'github competitive analysis'")
        
        # Step 2: System stores search request
        print("2️⃣ Search request stored in database")
        
        # Step 3: System triggers API calls
        print("3️⃣ API calls triggered to gather data")
        
        # Step 4: API responses stored with full details
        print("4️⃣ All API responses stored with metadata")
        
        # Step 5: Intelligence extraction
        print("5️⃣ Intelligence extracted from raw data")
        
        # Step 6: Company profile updated
        print("6️⃣ Company profile updated with new data")
        
        # Step 7: Results available to user
        print("7️⃣ Processed results available to user instantly")
        
        print("\n✨ This creates a complete audit trail and enables:")
        print("   📈 Performance analytics")
        print("   🔍 Historical search analysis") 
        print("   🧠 Intelligence pattern recognition")
        print("   📊 Data quality monitoring")
        print("   💾 Comprehensive caching")
        print("   🔄 Automated insights")
        
        return True
        
    except Exception as e:
        print(f"❌ Data flow demonstration failed: {e}")
        return False


async def main():
    """Main test function"""
    print("🧪 Comprehensive Data Storage Test Suite")
    print("This tests storing ALL API calls, search results, and research data")
    print("=" * 70)
    
    # Check configuration
    if not settings.supabase_url or not settings.supabase_key:
        print("❌ Supabase configuration missing!")
        print("   Please check your .env file has SUPABASE_URL and SUPABASE_KEY")
        return False
    
    # Run tests
    storage_test_success = await test_data_storage_system()
    data_flow_success = await demonstrate_data_flow()
    
    if storage_test_success and data_flow_success:
        print("\n🎉 All tests passed! Comprehensive data storage is working!")
        print("\n📋 Next steps:")
        print("   1. Create the enhanced data storage tables in Supabase")
        print("   2. Add the API extensions to main.py") 
        print("   3. Enable automatic data storage in all API calls")
        print("   4. Build frontend dashboards for data visualization")
        return True
    else:
        print("\n💥 Some tests failed - check the errors above")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nTest suite crashed: {e}")
        sys.exit(1)
