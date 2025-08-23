import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

import redis.asyncio as redis
from pydantic import BaseModel

from intelligence_engine.decision_orchestrator import IntelligenceEvent, EventType, Priority
from config.settings import settings


class EventPattern(BaseModel):
    pattern_id: str
    conditions: Dict[str, Any]
    trigger_threshold: int
    time_window_minutes: int
    severity_multiplier: float


class RealTimeEventProcessor:
    def __init__(self, decision_orchestrator):
        self.decision_orchestrator = decision_orchestrator
        self.redis_client = None
        self.pattern_matchers = self._initialize_patterns()
        self.event_cache = {}
        
    async def initialize(self):
        """Initialize Redis connection and event processing"""
        self.redis_client = redis.from_url(settings.redis_url)
        await self._setup_event_streams()
        
    async def _setup_event_streams(self):
        """Setup Redis streams for real-time event processing"""
        streams = [
            'brex_events',
            'pylon_events', 
            'sixtyfour_events',
            'mixrank_events',
            'system_events'
        ]
        
        for stream in streams:
            try:
                await self.redis_client.xgroup_create(
                    stream, 'cio_processors', id='0', mkstream=True
                )
            except redis.ResponseError:
                # Group already exists
                pass
                
    def _initialize_patterns(self) -> List[EventPattern]:
        """Initialize event patterns for detection"""
        return [
            # Cash flow patterns
            EventPattern(
                pattern_id="critical_cash_flow",
                conditions={"metric": "runway_days", "operator": "lt", "value": 30},
                trigger_threshold=1,
                time_window_minutes=60,
                severity_multiplier=2.0
            ),
            
            # Customer churn patterns
            EventPattern(
                pattern_id="churn_spike",
                conditions={"metric": "churn_rate", "operator": "gt", "value": 0.1},
                trigger_threshold=3,
                time_window_minutes=720,  # 12 hours
                severity_multiplier=1.5
            ),
            
            # Competitive threat patterns
            EventPattern(
                pattern_id="competitor_funding",
                conditions={"event_type": "funding_round", "amount": {"gt": 1000000}},
                trigger_threshold=1,
                time_window_minutes=1440,  # 24 hours
                severity_multiplier=1.3
            ),
            
            # Technical issue patterns
            EventPattern(
                pattern_id="service_degradation",
                conditions={"metric": "error_rate", "operator": "gt", "value": 0.05},
                trigger_threshold=5,
                time_window_minutes=30,
                severity_multiplier=1.8
            )
        ]
    
    async def start_processing(self):
        """Start the real-time event processing loop"""
        tasks = []
        
        # Start stream processors for each data source
        tasks.append(asyncio.create_task(self._process_brex_stream()))
        tasks.append(asyncio.create_task(self._process_pylon_stream()))
        tasks.append(asyncio.create_task(self._process_sixtyfour_stream()))
        tasks.append(asyncio.create_task(self._process_mixrank_stream()))
        
        # Start pattern detection processor
        tasks.append(asyncio.create_task(self._pattern_detection_loop()))
        
        # Start cache cleanup
        tasks.append(asyncio.create_task(self._cache_cleanup_loop()))
        
        await asyncio.gather(*tasks)
    
    async def _process_brex_stream(self):
        """Process Brex financial events"""
        while True:
            try:
                messages = await self.redis_client.xreadgroup(
                    'cio_processors', 'brex_consumer', 
                    {'brex_events': '>'}, count=10, block=1000
                )
                
                for stream, stream_messages in messages:
                    for message_id, fields in stream_messages:
                        await self._process_financial_event(fields)
                        
            except Exception as e:
                print(f"Error processing Brex stream: {e}")
                await asyncio.sleep(5)
    
    async def _process_pylon_stream(self):
        """Process Pylon customer events"""
        while True:
            try:
                messages = await self.redis_client.xreadgroup(
                    'cio_processors', 'pylon_consumer',
                    {'pylon_events': '>'}, count=10, block=1000
                )
                
                for stream, stream_messages in messages:
                    for message_id, fields in stream_messages:
                        await self._process_customer_event(fields)
                        
            except Exception as e:
                print(f"Error processing Pylon stream: {e}")
                await asyncio.sleep(5)
                
    async def _process_sixtyfour_stream(self):
        """Process SixtyFour market intelligence events"""
        while True:
            try:
                messages = await self.redis_client.xreadgroup(
                    'cio_processors', 'sixtyfour_consumer',
                    {'sixtyfour_events': '>'}, count=10, block=1000
                )
                
                for stream, stream_messages in messages:
                    for message_id, fields in stream_messages:
                        await self._process_market_event(fields)
                        
            except Exception as e:
                print(f"Error processing SixtyFour stream: {e}")
                await asyncio.sleep(5)
                
    async def _process_mixrank_stream(self):
        """Process MixRank technology intelligence events"""
        while True:
            try:
                messages = await self.redis_client.xreadgroup(
                    'cio_processors', 'mixrank_consumer',
                    {'mixrank_events': '>'}, count=10, block=1000
                )
                
                for stream, stream_messages in messages:
                    for message_id, fields in stream_messages:
                        await self._process_tech_event(fields)
                        
            except Exception as e:
                print(f"Error processing MixRank stream: {e}")
                await asyncio.sleep(5)
    
    async def _process_financial_event(self, event_data: Dict):
        """Process financial intelligence events from Brex"""
        try:
            data = json.loads(event_data.get('data', '{}'))
            
            # Detect critical financial situations
            if data.get('runway_days', float('inf')) < settings.critical_cash_runway_days:
                event = IntelligenceEvent(
                    event_type=EventType.FINANCIAL_ALERT,
                    priority=Priority.CRITICAL,
                    source='brex_mcp',
                    data=data,
                    timestamp=datetime.now(),
                    context=await self._get_business_context()
                )
                await self.decision_orchestrator.add_event(event)
                
        except Exception as e:
            print(f"Error processing financial event: {e}")
    
    async def _process_customer_event(self, event_data: Dict):
        """Process customer intelligence events from Pylon"""
        try:
            data = json.loads(event_data.get('data', '{}'))
            
            # Detect high-risk customer situations
            churn_risk = data.get('churn_risk_score', 0)
            if churn_risk > settings.high_churn_risk_threshold:
                event = IntelligenceEvent(
                    event_type=EventType.CUSTOMER_RISK,
                    priority=Priority.HIGH,
                    source='pylon_mcp',
                    data=data,
                    timestamp=datetime.now(),
                    context=await self._get_business_context()
                )
                await self.decision_orchestrator.add_event(event)
                
        except Exception as e:
            print(f"Error processing customer event: {e}")
    
    async def _process_market_event(self, event_data: Dict):
        """Process market intelligence events from SixtyFour"""
        try:
            data = json.loads(event_data.get('data', '{}'))
            
            # Detect market opportunities and threats
            opportunity_score = data.get('opportunity_score', 0)
            threat_score = data.get('threat_score', 0)
            
            if opportunity_score > 0.8:
                event = IntelligenceEvent(
                    event_type=EventType.MARKET_OPPORTUNITY,
                    priority=Priority.HIGH,
                    source='sixtyfour_mcp',
                    data=data,
                    timestamp=datetime.now(),
                    context=await self._get_business_context()
                )
                await self.decision_orchestrator.add_event(event)
                
            elif threat_score > settings.competitor_threat_threshold:
                event = IntelligenceEvent(
                    event_type=EventType.COMPETITIVE_THREAT,
                    priority=Priority.HIGH,
                    source='sixtyfour_mcp',
                    data=data,
                    timestamp=datetime.now(),
                    context=await self._get_business_context()
                )
                await self.decision_orchestrator.add_event(event)
                
        except Exception as e:
            print(f"Error processing market event: {e}")
    
    async def _process_tech_event(self, event_data: Dict):
        """Process technology intelligence events from MixRank"""
        try:
            data = json.loads(event_data.get('data', '{}'))
            
            # Detect competitive technology changes
            if data.get('competitor_tech_change'):
                event = IntelligenceEvent(
                    event_type=EventType.COMPETITIVE_THREAT,
                    priority=Priority.MEDIUM,
                    source='mixrank_mcp',
                    data=data,
                    timestamp=datetime.now(),
                    context=await self._get_business_context()
                )
                await self.decision_orchestrator.add_event(event)
                
        except Exception as e:
            print(f"Error processing tech event: {e}")
    
    async def _pattern_detection_loop(self):
        """Continuously analyze events for patterns"""
        while True:
            try:
                await self._analyze_event_patterns()
                await asyncio.sleep(60)  # Check patterns every minute
            except Exception as e:
                print(f"Error in pattern detection: {e}")
                await asyncio.sleep(60)
    
    async def _analyze_event_patterns(self):
        """Analyze cached events for concerning patterns"""
        for pattern in self.pattern_matchers:
            matching_events = self._find_matching_events(pattern)
            
            if len(matching_events) >= pattern.trigger_threshold:
                # Pattern detected, create synthetic event
                synthetic_event = IntelligenceEvent(
                    event_type=EventType.TECHNICAL_ISSUE,  # or determine dynamically
                    priority=Priority.HIGH,
                    source='pattern_detector',
                    data={
                        'pattern_id': pattern.pattern_id,
                        'matching_events': len(matching_events),
                        'severity': len(matching_events) * pattern.severity_multiplier
                    },
                    timestamp=datetime.now(),
                    context=await self._get_business_context()
                )
                
                await self.decision_orchestrator.add_event(synthetic_event)
    
    def _find_matching_events(self, pattern: EventPattern) -> List[Dict]:
        """Find events matching a specific pattern"""
        # Implementation for pattern matching logic
        matching_events = []
        cutoff_time = datetime.now() - timedelta(minutes=pattern.time_window_minutes)
        
        # Search through cached events
        for timestamp, events in self.event_cache.items():
            if datetime.fromisoformat(timestamp) > cutoff_time:
                for event in events:
                    if self._event_matches_pattern(event, pattern):
                        matching_events.append(event)
                        
        return matching_events
    
    def _event_matches_pattern(self, event: Dict, pattern: EventPattern) -> bool:
        """Check if an event matches a pattern's conditions"""
        # Implement pattern matching logic based on conditions
        return True  # Placeholder
    
    async def _get_business_context(self) -> Dict[str, Any]:
        """Get current business context for decision making"""
        # This would aggregate current metrics from all sources
        return {
            'runway_days': 120,  # Placeholder
            'customer_count': 1500,  # Placeholder
            'competitive_pressure': 'medium',  # Placeholder
            'growth_rate': 0.15  # Placeholder
        }
    
    async def _cache_cleanup_loop(self):
        """Clean up old events from cache"""
        while True:
            try:
                cutoff_time = datetime.now() - timedelta(days=7)
                cutoff_str = cutoff_time.isoformat()
                
                keys_to_remove = [
                    k for k in self.event_cache.keys() 
                    if k < cutoff_str
                ]
                
                for key in keys_to_remove:
                    del self.event_cache[key]
                    
                await asyncio.sleep(3600)  # Clean up every hour
                
            except Exception as e:
                print(f"Error in cache cleanup: {e}")
                await asyncio.sleep(3600)