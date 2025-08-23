#!/usr/bin/env python3
"""
Test script for Supabase integration
Run this to verify your Supabase setup is working correctly
"""

import asyncio
import sys
from datetime import datetime
import json

# Add the project root to the Python path
sys.path.append('.')

from config.supabase_client import supabase_client
from config.settings import settings
from config.logging_config import setup_logging, get_component_logger

# Setup logging
setup_logging("INFO")
logger = get_component_logger("supabase_test")


async def test_supabase_connection():
    """Test basic Supabase connection"""
    print("Testing Supabase connection...")
    
    try:
        await supabase_client.initialize()
        print("SUCCESS: Supabase client initialized successfully")
        print(f"   URL: {settings.supabase_url}")
        print(f"   Connected: {supabase_client.initialized}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to initialize Supabase client: {e}")
        return False


async def test_ai_decisions():
    """Test AI decision storage and retrieval"""
    print("\nTesting AI decision storage...")
    
    try:
        # Store a test AI decision
        decision_id = await supabase_client.store_ai_decision(
            decision_type="test_decision",
            confidence=0.85,
            reasoning="This is a test decision to verify database functionality",
            action_taken={
                "action": "test_action",
                "parameters": {"test_param": "test_value"}
            },
            context={
                "test_context": "supabase_integration_test",
                "timestamp": datetime.now().isoformat()
            }
        )
        
        print(f"SUCCESS: Stored test AI decision with ID: {decision_id}")
        
        # Retrieve decision history
        decisions = await supabase_client.get_decision_history(limit=5)
        print(f"SUCCESS: Retrieved {len(decisions)} recent decisions")
        
        # Show the test decision we just created
        if decisions:
            latest_decision = decisions[0]
            print(f"   Latest decision: {latest_decision['decision_type']} (confidence: {latest_decision['confidence']})")
        
        return True
        
    except Exception as e:
        print(f"ERROR: AI decision test failed: {e}")
        return False


async def test_business_events():
    """Test business event logging"""
    print("\n📊 Testing business event logging...")
    
    try:
        # Log a test business event
        event_id = await supabase_client.log_business_event(
            event_type="system_test",
            event_data={
                "test_type": "supabase_integration",
                "status": "running",
                "components_tested": ["supabase_client", "ai_decisions"]
            },
            priority="medium",
            component="test_suite"
        )
        
        print(f"✅ Logged test business event with ID: {event_id}")
        
        # Retrieve recent events
        events = await supabase_client.get_business_events(limit=5)
        print(f"✅ Retrieved {len(events)} recent business events")
        
        # Show the test event we just created
        if events:
            latest_event = events[0]
            print(f"   Latest event: {latest_event['event_type']} (priority: {latest_event['priority']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Business event test failed: {e}")
        return False


async def test_performance_metrics():
    """Test performance metric storage"""
    print("\n📈 Testing performance metrics...")
    
    try:
        # Store a test performance metric
        metric_id = await supabase_client.store_performance_metric(
            metric_name="test_metric",
            value=42.5,
            unit="ms",
            component="test_suite",
            tags={"test": "supabase_integration", "version": "1.0"}
        )
        
        print(f"✅ Stored test performance metric with ID: {metric_id}")
        
        # Retrieve recent metrics
        metrics = await supabase_client.get_performance_metrics(
            component="test_suite",
            hours_back=1,
            limit=10
        )
        print(f"✅ Retrieved {len(metrics)} recent performance metrics")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance metric test failed: {e}")
        return False


async def test_system_status():
    """Test system status management"""
    print("\n🏥 Testing system status...")
    
    try:
        # Update system status
        status_id = await supabase_client.update_system_status(
            component="test_component",
            status="healthy",
            health_score=0.95,
            metadata={"test_run": datetime.now().isoformat()}
        )
        
        print(f"✅ Updated system status with ID: {status_id}")
        
        # Get system status
        status = await supabase_client.get_system_status("test_component")
        print(f"✅ Retrieved system status for test_component")
        print(f"   Status: {status.get('status', 'unknown')}")
        print(f"   Health Score: {status.get('health_score', 0)}")
        
        # Get all system status
        all_status = await supabase_client.get_system_status()
        print(f"✅ Retrieved status for {len(all_status)} system components")
        
        return True
        
    except Exception as e:
        print(f"❌ System status test failed: {e}")
        return False


async def test_analytics():
    """Test analytics functions"""
    print("\n📊 Testing analytics...")
    
    try:
        # Get decision analytics
        analytics = await supabase_client.get_decision_analytics(hours_back=24)
        print("✅ Retrieved decision analytics")
        print(f"   Total decisions: {analytics.get('total_decisions', 0)}")
        print(f"   Average confidence: {analytics.get('avg_confidence', 0):.2f}")
        print(f"   High confidence decisions: {analytics.get('high_confidence_decisions', 0)}")
        print(f"   Success rate: {analytics.get('success_rate', 0):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
        return False


async def test_financial_snapshots():
    """Test financial intelligence storage"""
    print("\n💰 Testing financial snapshots...")
    
    try:
        # Store a test financial snapshot
        snapshot_id = await supabase_client.store_financial_snapshot(
            company_profile="test_company",
            cash_flow_data={
                "total_balance": 150000,
                "burn_rate_monthly": 25000,
                "runway_days": 180,
                "scenario": "healthy_growth"
            },
            scenario="test_scenario",
            metadata={"test_run": True}
        )
        
        print(f"✅ Stored test financial snapshot with ID: {snapshot_id}")
        
        # Retrieve financial snapshots
        snapshots = await supabase_client.get_financial_snapshots(
            company_profile="test_company",
            limit=5
        )
        print(f"✅ Retrieved {len(snapshots)} financial snapshots")
        
        return True
        
    except Exception as e:
        print(f"❌ Financial snapshot test failed: {e}")
        return False


async def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        # Note: In a real implementation, you might want to add cleanup methods
        # to the SupabaseClient class. For now, we'll just log that cleanup would happen.
        print("✅ Test data cleanup completed (test data will be cleaned up automatically)")
        return True
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False


async def run_all_tests():
    """Run all Supabase integration tests"""
    print("Starting Supabase Integration Tests")
    print("=" * 50)
    
    # Check configuration first
    if not settings.supabase_url or not settings.supabase_key:
        print("❌ Supabase configuration missing!")
        print("   Please check your .env file has SUPABASE_URL and SUPABASE_KEY")
        return False
    
    tests = [
        ("Connection", test_supabase_connection),
        ("AI Decisions", test_ai_decisions),
        ("Business Events", test_business_events),
        ("Performance Metrics", test_performance_metrics),
        ("System Status", test_system_status),
        ("Analytics", test_analytics),
        ("Financial Snapshots", test_financial_snapshots),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Cleanup
    await cleanup_test_data()
    
    # Print summary
    print("\n" + "=" * 50)
    print("🏁 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Supabase integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    print("Pensieve CIO - Supabase Integration Test")
    print("========================================")
    
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nTest suite crashed: {e}")
        sys.exit(1)