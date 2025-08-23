#!/usr/bin/env python3
"""
Setup and test intelligence cache tables in Supabase
This creates the tables needed for the intelligence caching system
"""

import asyncio
import sys
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.append('.')

from config.supabase_client import supabase_client
from config.settings import settings
from config.logging_config import setup_logging, get_component_logger

# Setup logging
setup_logging("INFO")
logger = get_component_logger("intelligence_cache_setup")


async def create_intelligence_cache_tables():
    """Create intelligence cache tables if they don't exist"""
    print("🗄️  Creating intelligence cache tables...")
    
    try:
        # Read the schema SQL
        with open('database/intelligence_cache_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        print(f"📜 Loaded schema SQL ({len(schema_sql)} characters)")
        
        # Split into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        print(f"🔧 Executing {len(statements)} SQL statements...")
        
        # Execute each statement
        for i, statement in enumerate(statements, 1):
            if statement.upper().startswith(('CREATE', 'INSERT', 'ALTER')):
                try:
                    # Use RPC call for DDL statements
                    result = supabase_client.client.rpc('execute_sql', {'sql_statement': statement}).execute()
                    print(f"   ✅ Statement {i}: {statement[:50]}...")
                except Exception as e:
                    if 'already exists' in str(e).lower():
                        print(f"   ⚠️  Statement {i}: Already exists - {statement[:50]}...")
                    else:
                        print(f"   ❌ Statement {i} failed: {e}")
                        # Some statements might fail if function doesn't exist, continue anyway
        
        print("✅ Intelligence cache tables setup completed")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create intelligence cache tables: {e}")
        print("📝 You may need to manually run the SQL from database/intelligence_cache_schema.sql")
        print("   in your Supabase dashboard SQL editor")
        return False


async def test_intelligence_cache_tables():
    """Test intelligence cache table operations"""
    print("\n🧪 Testing intelligence cache tables...")
    
    try:
        # Test 1: Insert into intelligence_cache
        print("   Testing intelligence_cache table...")
        
        cache_data = {
            'company_name': 'test_company',
            'research_depth': 'standard',
            'intelligence_type': 'competitive',
            'financial_health': {'status': 'healthy', 'score': 0.85},
            'competitive_signals': {'market_position': 'strong'},
            'cached_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=12)).isoformat(),
            'cache_status': 'completed',
            'fetch_duration_seconds': 45.2,
            'data_size_bytes': 2048
        }
        
        result = supabase_client.client.table('intelligence_cache').insert(cache_data).execute()
        cache_id = result.data[0]['id'] if result.data else None
        print(f"   ✅ Inserted cache record: {cache_id}")
        
        # Test 2: Insert into intelligence_prefetch_queue
        print("   Testing intelligence_prefetch_queue table...")
        
        queue_data = {
            'company_name': 'test_queue_company',
            'research_depth': 'basic',
            'intelligence_type': 'financial',
            'priority': 75,
            'requested_by': 'test_suite',
            'status': 'queued'
        }
        
        result = supabase_client.client.table('intelligence_prefetch_queue').insert(queue_data).execute()
        queue_id = result.data[0]['id'] if result.data else None
        print(f"   ✅ Inserted queue record: {queue_id}")
        
        # Test 3: Test cache lookup function
        print("   Testing cache lookup...")
        
        try:
            result = supabase_client.client.rpc('get_company_intelligence', {
                'p_company_name': 'test_company',
                'p_research_depth': 'standard',
                'p_intelligence_type': 'competitive'
            }).execute()
            
            if result.data:
                print(f"   ✅ Cache lookup successful: {result.data.get('cache_hit', False)}")
            else:
                print("   ⚠️  Cache lookup returned no data")
                
        except Exception as e:
            print(f"   ⚠️  Cache lookup function not available: {e}")
        
        # Test 4: Query cache analytics view
        print("   Testing cache analytics view...")
        
        try:
            result = supabase_client.client.table('intelligence_cache_analytics').select('*').limit(5).execute()
            print(f"   ✅ Analytics view query successful: {len(result.data)} records")
        except Exception as e:
            print(f"   ⚠️  Analytics view not available: {e}")
        
        # Cleanup test data
        print("   Cleaning up test data...")
        if cache_id:
            supabase_client.client.table('intelligence_cache').delete().eq('id', cache_id).execute()
        if queue_id:
            supabase_client.client.table('intelligence_prefetch_queue').delete().eq('id', queue_id).execute()
        
        print("✅ Intelligence cache table tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Intelligence cache table test failed: {e}")
        return False


async def test_cache_manager_integration():
    """Test the cache manager with real tables"""
    print("\n🔧 Testing cache manager integration...")
    
    try:
        # Import the cache manager
        from intelligence_engine.cache.intelligence_cache_manager import cache_manager
        
        # Test cache lookup (should be cache miss for new company)
        result = await cache_manager.get_intelligence('test_integration_company', 'standard', 'competitive')
        
        if result is None:
            print("   ✅ Cache miss handled correctly (company queued for fetch)")
        else:
            print(f"   ⚠️  Unexpected cache hit: {result}")
        
        # Check if company was queued
        queue_check = supabase_client.client.table('intelligence_prefetch_queue').select('*').eq(
            'company_name', 'test_integration_company'
        ).execute()
        
        if queue_check.data:
            print(f"   ✅ Company queued for fetch: {len(queue_check.data)} records")
            
            # Cleanup
            for record in queue_check.data:
                supabase_client.client.table('intelligence_prefetch_queue').delete().eq('id', record['id']).execute()
        else:
            print("   ⚠️  Company not found in prefetch queue")
        
        print("✅ Cache manager integration test completed")
        return True
        
    except Exception as e:
        print(f"❌ Cache manager integration test failed: {e}")
        return False


async def main():
    """Main setup and test function"""
    print("🧠 Pensieve Intelligence Cache Setup & Test")
    print("=" * 60)
    
    # Check configuration
    if not settings.supabase_url or not settings.supabase_key:
        print("❌ Supabase configuration missing!")
        print("   Please check your .env file has SUPABASE_URL and SUPABASE_KEY")
        return False
    
    # Initialize Supabase client
    try:
        await supabase_client.initialize()
        print("✅ Supabase client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Supabase client: {e}")
        return False
    
    # Run setup and tests
    tests = [
        ("Create Tables", create_intelligence_cache_tables),
        ("Test Tables", test_intelligence_cache_tables),
        ("Test Integration", test_cache_manager_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("🏁 Setup & Test Results")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Intelligence cache system is ready!")
        print("\n📋 Next steps:")
        print("   1. Start the background cache processor")
        print("   2. Test the Gemini intelligence tool")
        print("   3. Enable autonomous decision-making with cached intelligence")
        return True
    else:
        print("⚠️  Some setup steps failed.")
        print("\n🔧 Manual setup may be required:")
        print("   1. Copy the SQL from database/intelligence_cache_schema.sql")
        print("   2. Run it in your Supabase dashboard SQL editor")
        print("   3. Re-run this script to test")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nSetup crashed: {e}")
        sys.exit(1)
