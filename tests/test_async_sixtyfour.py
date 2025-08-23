#!/usr/bin/env python3
"""
Test async SixtyFour API with job submission and polling (no timeout blocking)
"""

import os
import sys
import asyncio
import time

# Add the specific directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp-servers', 'sixtyfour-mcp'))

from sixtyfour_api_client import (
    submit_enrich_job, 
    get_job_status, 
    get_job_result,
    wait_for_job,
    JobStatus,
    SixtyFourAPIError
)

async def test_async_job_submission():
    """Test the new async job pattern"""
    print("🚀 Testing Async SixtyFour Job Submission")
    print("=" * 50)
    
    # Set API key
    os.environ['SIXTYFOUR_API_KEY'] = "yj9TfC1UL5MFUpVmjjpb4rCtErtoPaYk"
    
    # Submit a job for deep intelligence (this will take 5+ minutes)
    lead_info = {
        "company": "stripe",
        "research_depth": "maximum",  # Use maximum for comprehensive data
        "intelligence_type": "competitive"
    }
    
    struct = {
        "financial_health": "Payment patterns, hiring velocity, cash flow signals",
        "competitive_signals": "Customer migration, pricing intelligence, market position", 
        "strategic_shifts": "Product pivots, market repositioning, technology adoption",
        "customer_intelligence": "Expansion patterns, integration depth, renewal risks",
        "market_opportunities": "Growth areas, acquisition targets, market gaps"
    }
    
    try:
        # Submit job (returns immediately)
        print(f"📤 Submitting deep intelligence job for {lead_info['company']}...")
        job_id = submit_enrich_job(lead_info, struct)
        print(f"✅ Job submitted! ID: {job_id}")
        
        # Check status immediately
        job = get_job_status(job_id)
        print(f"📊 Initial status: {job.status.value}")
        
        # Option 1: Poll manually
        print("\n⏱️  Manual polling (every 30 seconds):")
        for i in range(12):  # Check for up to 6 minutes
            await asyncio.sleep(30)  # Wait 30 seconds
            
            job = get_job_status(job_id)
            elapsed = time.time() - job.submitted_at
            print(f"   [{elapsed:.0f}s] Status: {job.status.value}")
            
            if job.status == JobStatus.COMPLETED:
                result = get_job_result(job_id)
                print(f"🎉 Job completed! Got {len(result)} result fields")
                print(f"📄 Result keys: {list(result.keys()) if result else 'No result'}")
                
                if result:
                    # Show some sample data
                    for key, value in list(result.items())[:3]:
                        preview = str(value)[:150] + ("..." if len(str(value)) > 150 else "")
                        print(f"   {key}: {preview}")
                
                return True
                
            elif job.status == JobStatus.FAILED:
                print(f"❌ Job failed: {job.error}")
                return False
        
        print("⏰ Job still processing after 6 minutes - this is normal for deep intelligence")
        
        # Option 2: Use wait_for_job (will wait indefinitely)
        print("\n🔄 Using wait_for_job() to wait until completion...")
        result = await wait_for_job(job_id, poll_interval=60.0)  # Poll every minute
        
        print(f"🎉 Final result received! {len(result)} fields")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"📜 Traceback: {traceback.format_exc()}")
        return False


async def test_quick_job():
    """Test with a quicker job for comparison"""
    print("\n🏃 Testing Quick Job (basic research)")
    print("=" * 30)
    
    lead_info = {
        "company": "github",
        "research_depth": "basic"  # Should be faster
    }
    
    struct = {
        "company_overview": "Basic company information",
        "market_position": "Current market standing"
    }
    
    try:
        job_id = submit_enrich_job(lead_info, struct)
        print(f"📤 Submitted quick job: {job_id}")
        
        # Wait for this one since it should be faster
        result = await wait_for_job(job_id, poll_interval=15.0)
        print(f"✅ Quick job completed! Keys: {list(result.keys()) if result else 'No result'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick job failed: {e}")
        return False


async def main():
    """Run the async tests"""
    print("🔬 Async SixtyFour API Test Suite")
    print("This will submit jobs and poll for results without blocking")
    print("Deep intelligence jobs can take 5+ minutes")
    print("=" * 60)
    
    # Test 1: Full deep intelligence job
    success1 = await test_async_job_submission()
    
    # Test 2: Quick job
    success2 = await test_quick_job()
    
    print(f"\n📊 Results: Deep job: {success1}, Quick job: {success2}")
    
    if success1 or success2:
        print("🎉 Async pattern working! No more timeout blocking.")
    else:
        print("💥 Both tests failed")


if __name__ == '__main__':
    # Run the async test
    asyncio.run(main())
