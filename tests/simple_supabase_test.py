#!/usr/bin/env python3
"""
Simple Supabase connection test without emoji characters
Run this to verify your Supabase setup is working
"""

import asyncio
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.append('.')

from config.supabase_client import supabase_client
from config.settings import settings


async def test_connection():
    """Test basic Supabase connection"""
    print("Testing Supabase connection...")
    print(f"URL: {settings.supabase_url}")
    
    try:
        await supabase_client.initialize()
        print("SUCCESS: Supabase client initialized successfully")
        print(f"Connected: {supabase_client.initialized}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to initialize Supabase client: {e}")
        return False


async def test_basic_operations():
    """Test basic database operations"""
    print("\nTesting basic database operations...")
    
    try:
        # Test AI decision storage
        decision_id = await supabase_client.store_ai_decision(
            decision_type="connection_test",
            confidence=0.95,
            reasoning="Testing database connection and basic functionality",
            action_taken={"action": "connection_test", "status": "success"},
            context={"test_type": "connection_test", "timestamp": datetime.now().isoformat()}
        )
        print(f"SUCCESS: Stored AI decision with ID: {decision_id}")
        
        # Test business event logging
        event_id = await supabase_client.log_business_event(
            event_type="connection_test",
            event_data={"status": "testing", "component": "supabase_client"},
            priority="low",
            component="test_suite"
        )
        print(f"SUCCESS: Logged business event with ID: {event_id}")
        
        # Test system status update
        await supabase_client.update_system_status(
            component="test_component",
            status="healthy",
            health_score=1.0
        )
        print("SUCCESS: Updated system status")
        
        # Test data retrieval
        decisions = await supabase_client.get_decision_history(limit=3)
        events = await supabase_client.get_business_events(limit=3)
        status = await supabase_client.get_system_status()
        
        print(f"SUCCESS: Retrieved {len(decisions)} decisions")
        print(f"SUCCESS: Retrieved {len(events)} business events")
        print(f"SUCCESS: Retrieved {len(status)} system status records")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Basic operations failed: {e}")
        return False


async def main():
    """Main test function"""
    print("Pensieve CIO - Supabase Connection Test")
    print("=" * 50)
    
    # Check configuration
    if not settings.supabase_url or not settings.supabase_key:
        print("ERROR: Supabase configuration missing!")
        print("Please check your .env file has SUPABASE_URL and SUPABASE_KEY")
        return False
    
    # Test connection
    connection_ok = await test_connection()
    if not connection_ok:
        print("\nFAILED: Could not connect to Supabase")
        return False
    
    # Test basic operations
    operations_ok = await test_basic_operations()
    if not operations_ok:
        print("\nFAILED: Database operations failed")
        print("This might mean the database schema is not set up yet.")
        print("Please run the SQL schema from database/supabase_schema.sql in your Supabase dashboard")
        return False
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("Supabase integration is working correctly.")
    print("You can now run the full Pensieve CIO system.")
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest crashed: {e}")
        sys.exit(1)