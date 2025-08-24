"""
Intelligence Cache Manager for SixtyFour Data

Handles caching, pre-fetching, and instant access to company intelligence data.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

from config.settings import settings
from config.supabase_client import supabase_client
from config.logging_config import get_component_logger
import sys
import os
# Fix path to find mcp_servers
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import from mcp-servers directory with hyphen
sys.path.insert(0, os.path.join(project_root, 'mcp-servers', 'sixtyfour-mcp'))
from sixtyfour_api_client import (
    submit_enrich_job, 
    get_job_status, 
    get_job_result,
    JobStatus,
    SixtyFourAPIError
)

logger = get_component_logger("intelligence_cache")


class CacheStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed" 
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass
class CacheEntry:
    """Represents a cached intelligence entry"""
    company_name: str
    research_depth: str
    intelligence_type: str
    data: Dict[str, Any]
    cached_at: datetime
    expires_at: datetime
    access_count: int = 0


class IntelligenceCacheManager:
    """Manages intelligent caching and pre-fetching of company data"""
    
    def __init__(self):
        self.logger = get_component_logger("intelligence_cache")
        self._background_tasks = set()
        
        # Cache configuration
        self.default_ttl_hours = {
            'basic': 24,      # Basic data expires in 1 day
            'standard': 12,   # Standard data expires in 12 hours  
            'maximum': 6      # Deep intelligence expires in 6 hours
        }
        
        # Pre-fetch priorities for common companies
        self.high_priority_companies = [
            'stripe', 'openai', 'anthropic', 'github', 'microsoft', 
            'google', 'meta', 'amazon', 'apple', 'salesforce'
        ]
    
    async def get_intelligence(
        self, 
        company_name: str, 
        research_depth: str = 'standard',
        intelligence_type: str = 'competitive'
    ) -> Optional[Dict[str, Any]]:
        """Get intelligence data with cache-first approach"""
        
        self.logger.info(f"Getting intelligence for {company_name} (depth: {research_depth})")
        
        # Try cache first
        cached_data = await self._get_from_cache(company_name, research_depth, intelligence_type)
        if cached_data:
            self.logger.info(f"Cache hit for {company_name}")
            return cached_data
        
        # Cache miss - check if already queued for fetch
        if await self._is_queued_for_fetch(company_name, research_depth, intelligence_type):
            self.logger.info(f"Already queued for fetch: {company_name}")
            return None
        
        # Queue for high-priority fetch
        await self._queue_for_fetch(
            company_name, research_depth, intelligence_type, 
            priority=80, requested_by='on_demand'
        )
        
        return None
    
    async def _get_from_cache(
        self, 
        company_name: str, 
        research_depth: str, 
        intelligence_type: str
    ) -> Optional[Dict[str, Any]]:
        """Get data from Supabase cache"""
        
        try:
            response = await supabase_client.client.table('intelligence_cache').select('*').eq(
                'company_name', company_name.lower()
            ).eq(
                'research_depth', research_depth
            ).eq(
                'intelligence_type', intelligence_type
            ).eq(
                'cache_status', 'completed'
            ).gt(
                'expires_at', datetime.now().isoformat()
            ).order('cached_at', desc=True).limit(1).execute()
            
            if response.data:
                cache_record = response.data[0]
                
                # Update access tracking
                await supabase_client.client.table('intelligence_cache').update({
                    'last_accessed_at': datetime.now().isoformat(),
                    'access_count': cache_record['access_count'] + 1
                }).eq('id', cache_record['id']).execute()
                
                # Build result from cached fields
                return {
                    'financial_health': cache_record.get('financial_health'),
                    'competitive_signals': cache_record.get('competitive_signals'),
                    'strategic_shifts': cache_record.get('strategic_shifts'),
                    'customer_intelligence': cache_record.get('customer_intelligence'),
                    'market_opportunities': cache_record.get('market_opportunities'),
                    'insider_threats': cache_record.get('insider_threats'),
                    'regulatory_risks': cache_record.get('regulatory_risks'),
                    'cached_at': cache_record['cached_at'],
                    'cache_hit': True
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Cache lookup failed for {company_name}: {e}")
            return None
    
    async def _is_queued_for_fetch(
        self, 
        company_name: str, 
        research_depth: str, 
        intelligence_type: str
    ) -> bool:
        """Check if company is already queued for fetch"""
        
        try:
            response = await supabase_client.client.table('intelligence_prefetch_queue').select('id').eq(
                'company_name', company_name.lower()
            ).eq(
                'research_depth', research_depth
            ).eq(
                'intelligence_type', intelligence_type
            ).in_('status', ['queued', 'processing']).execute()
            
            return len(response.data) > 0
            
        except Exception as e:
            self.logger.error(f"Queue lookup failed: {e}")
            return False
    
    async def _queue_for_fetch(
        self, 
        company_name: str, 
        research_depth: str, 
        intelligence_type: str,
        priority: int = 50,
        requested_by: str = 'system'
    ):
        """Queue company for intelligence fetch"""
        
        try:
            await supabase_client.client.table('intelligence_prefetch_queue').upsert({
                'company_name': company_name.lower(),
                'research_depth': research_depth,
                'intelligence_type': intelligence_type,
                'priority': priority,
                'requested_by': requested_by,
                'requested_at': datetime.now().isoformat(),
                'status': 'queued'
            }).execute()
            
            self.logger.info(f"Queued {company_name} for fetch (priority: {priority})")
            
        except Exception as e:
            self.logger.error(f"Failed to queue {company_name}: {e}")
    
    async def start_background_processor(self):
        """Start background task for processing pre-fetch queue"""
        
        self.logger.info("Starting background intelligence processor")
        
        while True:
            try:
                await self._process_prefetch_queue()
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Background processor error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _process_prefetch_queue(self):
        """Process the highest priority items in prefetch queue"""
        
        try:
            # Get next batch of items to process (limit concurrent jobs)
            response = await supabase_client.client.table('intelligence_prefetch_queue').select('*').eq(
                'status', 'queued'
            ).lte(
                'schedule_after', datetime.now().isoformat()
            ).order('priority', desc=True).order('requested_at').limit(5).execute()
            
            for queue_item in response.data:
                # Mark as processing
                await supabase_client.client.table('intelligence_prefetch_queue').update({
                    'status': 'processing',
                    'processing_started_at': datetime.now().isoformat()
                }).eq('id', queue_item['id']).execute()
                
                # Start background fetch
                task = asyncio.create_task(
                    self._fetch_and_cache_intelligence(queue_item)
                )
                self._background_tasks.add(task)
                task.add_done_callback(self._background_tasks.discard)
                
        except Exception as e:
            self.logger.error(f"Queue processing error: {e}")
    
    async def _fetch_and_cache_intelligence(self, queue_item: Dict[str, Any]):
        """Fetch intelligence data and store in cache"""
        
        company_name = queue_item['company_name']
        research_depth = queue_item['research_depth'] 
        intelligence_type = queue_item['intelligence_type']
        
        self.logger.info(f"Fetching intelligence for {company_name}")
        
        try:
            # Create cache record
            cache_id = await self._create_cache_record(
                company_name, research_depth, intelligence_type
            )
            
            # Submit SixtyFour job
            lead_info = {
                'company': company_name,
                'research_depth': research_depth,
                'intelligence_type': intelligence_type
            }
            
            struct = self._build_intelligence_struct(intelligence_type)
            job_id = submit_enrich_job(lead_info, struct)
            
            # Update cache record with job ID
            await supabase_client.client.table('intelligence_cache').update({
                'sixtyfour_job_id': job_id,
                'cache_status': 'processing'
            }).eq('id', cache_id).execute()
            
            # Wait for job completion (with timeout)
            start_time = time.time()
            max_wait_time = 600  # 10 minutes max
            
            while time.time() - start_time < max_wait_time:
                job_status = get_job_status(job_id)
                
                if job_status.status == JobStatus.COMPLETED:
                    # Store the result
                    result = get_job_result(job_id)
                    await self._store_intelligence_result(cache_id, result, start_time)
                    
                    # Mark queue item as completed
                    await self._mark_queue_completed(queue_item['id'])
                    
                    self.logger.info(f"Successfully cached intelligence for {company_name}")
                    return
                    
                elif job_status.status == JobStatus.FAILED:
                    await self._mark_cache_failed(cache_id, job_status.error)
                    await self._mark_queue_failed(queue_item['id'], job_status.error)
                    return
                
                await asyncio.sleep(30)  # Poll every 30 seconds
            
            # Timeout
            await self._mark_cache_failed(cache_id, "Fetch timeout after 10 minutes")
            await self._mark_queue_failed(queue_item['id'], "Timeout")
            
        except Exception as e:
            self.logger.error(f"Failed to fetch intelligence for {company_name}: {e}")
            await self._mark_queue_failed(queue_item['id'], str(e))
    
    def _build_intelligence_struct(self, intelligence_type: str) -> Dict[str, str]:
        """Build the struct for SixtyFour based on intelligence type"""
        
        if intelligence_type == 'competitive':
            return {
                "financial_health": "Payment patterns, hiring velocity, cash flow signals",
                "competitive_signals": "Customer migration, pricing intelligence, market position", 
                "strategic_shifts": "Product pivots, market repositioning, technology adoption",
                "customer_intelligence": "Expansion patterns, integration depth, renewal risks",
                "market_opportunities": "Growth areas, acquisition targets, market gaps"
            }
        elif intelligence_type == 'financial':
            return {
                "financial_health": "Cash flow, runway, burn rate, revenue trends",
                "insider_threats": "Financial irregularities, audit problems", 
                "regulatory_risks": "Compliance issues, regulatory changes"
            }
        else:
            return {
                "competitive_signals": "Basic competitive intelligence",
                "market_opportunities": "Basic market analysis"
            }
    
    async def _create_cache_record(
        self, 
        company_name: str, 
        research_depth: str, 
        intelligence_type: str
    ) -> str:
        """Create initial cache record"""
        
        ttl_hours = self.default_ttl_hours.get(research_depth, 12)
        expires_at = datetime.now() + timedelta(hours=ttl_hours)
        
        response = await supabase_client.client.table('intelligence_cache').insert({
            'company_name': company_name.lower(),
            'research_depth': research_depth,
            'intelligence_type': intelligence_type,
            'cached_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'cache_status': 'pending'
        }).execute()
        
        return response.data[0]['id']
    
    async def _store_intelligence_result(
        self, 
        cache_id: str, 
        result: Dict[str, Any], 
        start_time: float
    ):
        """Store the intelligence result in cache"""
        
        fetch_duration = time.time() - start_time
        data_size = len(json.dumps(result).encode('utf-8'))
        
        update_data = {
            'financial_health': result.get('financial_health'),
            'competitive_signals': result.get('competitive_signals'),
            'strategic_shifts': result.get('strategic_shifts'),
            'customer_intelligence': result.get('customer_intelligence'),
            'market_opportunities': result.get('market_opportunities'),
            'insider_threats': result.get('insider_threats'),
            'regulatory_risks': result.get('regulatory_risks'),
            'raw_response': result,
            'cache_status': 'completed',
            'fetch_duration_seconds': fetch_duration,
            'data_size_bytes': data_size
        }
        
        await supabase_client.client.table('intelligence_cache').update(
            update_data
        ).eq('id', cache_id).execute()
    
    async def _mark_cache_failed(self, cache_id: str, error: str):
        """Mark cache record as failed"""
        
        await supabase_client.client.table('intelligence_cache').update({
            'cache_status': 'failed',
            'error_message': error
        }).eq('id', cache_id).execute()
    
    async def _mark_queue_completed(self, queue_id: str):
        """Mark queue item as completed"""
        
        await supabase_client.client.table('intelligence_prefetch_queue').update({
            'status': 'completed',
            'completed_at': datetime.now().isoformat()
        }).eq('id', queue_id).execute()
    
    async def _mark_queue_failed(self, queue_id: str, error: str):
        """Mark queue item as failed"""
        
        await supabase_client.client.table('intelligence_prefetch_queue').update({
            'status': 'failed',
            'completed_at': datetime.now().isoformat(),
            'retry_count': supabase_client.client.table('intelligence_prefetch_queue').select('retry_count').eq('id', queue_id).execute().data[0]['retry_count'] + 1
        }).eq('id', queue_id).execute()
    
    async def prefetch_high_priority_companies(self):
        """Pre-fetch intelligence for high-priority companies"""
        
        self.logger.info("Pre-fetching high-priority companies")
        
        for company in self.high_priority_companies:
            for research_depth in ['standard', 'maximum']:
                for intel_type in ['competitive', 'financial']:
                    await self._queue_for_fetch(
                        company, research_depth, intel_type,
                        priority=90, requested_by='priority_prefetch'
                    )
        
        self.logger.info(f"Queued {len(self.high_priority_companies)} companies for prefetch")


# Global cache manager instance
cache_manager = IntelligenceCacheManager()
