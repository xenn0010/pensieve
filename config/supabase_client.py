import asyncio
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import logging

from supabase import create_client, Client
from config.settings import settings
from config.logging_config import get_component_logger

logger = get_component_logger("supabase_client")


class SupabaseClient:
    """Production-ready Supabase client for Pensieve CIO"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.initialized = False
        
    async def initialize(self):
        """Initialize Supabase client connection"""
        try:
            if not settings.supabase_url:
                raise ValueError("Supabase URL is required")
            
            # Use service key if available for write operations, otherwise use anon key
            key_to_use = settings.supabase_service_key if settings.supabase_service_key else settings.supabase_key
            if not key_to_use:
                raise ValueError("Either Supabase service key or anon key is required")
            
            # Create Supabase client
            self.client = create_client(
                settings.supabase_url,
                key_to_use
            )
            
            # Test connection
            await self._test_connection()
            
            self.initialized = True
            logger.info("Supabase client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise
    
    async def _test_connection(self):
        """Test Supabase connection"""
        try:
            # Simple query to test connection
            result = self.client.table('_health_check').select('*').limit(1).execute()
            logger.info("Supabase connection test successful")
        except Exception as e:
            # Table might not exist, that's ok for connection test
            logger.info("Supabase connection established")
    
    def ensure_initialized(self):
        """Ensure client is initialized"""
        if not self.initialized or not self.client:
            raise RuntimeError("Supabase client not initialized. Call initialize() first.")
    
    # AI Decision History
    async def store_ai_decision(
        self, 
        decision_type: str,
        confidence: float,
        reasoning: str,
        action_taken: Dict[str, Any],
        context: Dict[str, Any],
        outcome: Optional[str] = None
    ) -> str:
        """Store AI decision in database"""
        self.ensure_initialized()
        
        try:
            decision_data = {
                'decision_type': decision_type,
                'confidence': confidence,
                'reasoning': reasoning,
                'action_taken': action_taken,
                'context': context,
                'outcome': outcome,
                'created_at': datetime.now().isoformat(),
                'component': 'decision_orchestrator'
            }
            
            result = self.client.table('ai_decisions').insert(decision_data).execute()
            
            decision_id = result.data[0]['id'] if result.data else None
            logger.info(f"Stored AI decision: {decision_type} (ID: {decision_id})")
            
            return decision_id
            
        except Exception as e:
            logger.error(f"Error storing AI decision: {e}")
            raise
    
    async def get_decision_history(
        self,
        limit: int = 100,
        decision_type: Optional[str] = None,
        min_confidence: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get AI decision history"""
        self.ensure_initialized()
        
        try:
            query = self.client.table('ai_decisions').select('*')
            
            if decision_type:
                query = query.eq('decision_type', decision_type)
            
            if min_confidence:
                query = query.gte('confidence', min_confidence)
            
            result = query.order('created_at', desc=True).limit(limit).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting decision history: {e}")
            raise
    
    # Business Events
    async def log_business_event(
        self,
        event_type: str,
        event_data: Dict[str, Any],
        priority: str = 'medium',
        component: str = 'system',
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Log business event to database"""
        self.ensure_initialized()
        
        try:
            event_record = {
                'event_type': event_type,
                'event_data': event_data,
                'priority': priority,
                'component': component,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat()
            }
            
            result = self.client.table('business_events').insert(event_record).execute()
            
            event_id = result.data[0]['id'] if result.data else None
            logger.info(f"Logged business event: {event_type} (ID: {event_id})")
            
            return event_id
            
        except Exception as e:
            logger.error(f"Error logging business event: {e}")
            raise
    
    async def get_business_events(
        self,
        limit: int = 100,
        event_type: Optional[str] = None,
        priority: Optional[str] = None,
        component: Optional[str] = None,
        hours_back: Optional[int] = 24
    ) -> List[Dict[str, Any]]:
        """Get business events"""
        self.ensure_initialized()
        
        try:
            query = self.client.table('business_events').select('*')
            
            if event_type:
                query = query.eq('event_type', event_type)
            
            if priority:
                query = query.eq('priority', priority)
            
            if component:
                query = query.eq('component', component)
            
            if hours_back:
                from datetime import timedelta
                cutoff_time = datetime.now() - timedelta(hours=hours_back)
                query = query.gte('created_at', cutoff_time.isoformat())
            
            result = query.order('created_at', desc=True).limit(limit).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting business events: {e}")
            raise
    
    # Performance Metrics
    async def store_performance_metric(
        self,
        metric_name: str,
        value: float,
        unit: Optional[str] = None,
        component: str = 'system',
        tags: Optional[Dict[str, str]] = None
    ) -> str:
        """Store performance metric"""
        self.ensure_initialized()
        
        try:
            metric_data = {
                'metric_name': metric_name,
                'value': value,
                'unit': unit,
                'component': component,
                'tags': tags or {},
                'timestamp': datetime.now().isoformat()
            }
            
            result = self.client.table('performance_metrics').insert(metric_data).execute()
            
            metric_id = result.data[0]['id'] if result.data else None
            logger.debug(f"Stored performance metric: {metric_name}={value}")
            
            return metric_id
            
        except Exception as e:
            logger.error(f"Error storing performance metric: {e}")
            raise
    
    async def get_performance_metrics(
        self,
        metric_name: Optional[str] = None,
        component: Optional[str] = None,
        hours_back: int = 24,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """Get performance metrics"""
        self.ensure_initialized()
        
        try:
            query = self.client.table('performance_metrics').select('*')
            
            if metric_name:
                query = query.eq('metric_name', metric_name)
            
            if component:
                query = query.eq('component', component)
            
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            query = query.gte('timestamp', cutoff_time.isoformat())
            
            result = query.order('timestamp', desc=True).limit(limit).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            raise
    
    # Financial Intelligence Data
    async def store_financial_snapshot(
        self,
        company_profile: str,
        cash_flow_data: Dict[str, Any],
        scenario: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store financial intelligence snapshot"""
        self.ensure_initialized()
        
        try:
            snapshot_data = {
                'company_profile': company_profile,
                'cash_flow_data': cash_flow_data,
                'scenario': scenario,
                'metadata': metadata or {},
                'captured_at': datetime.now().isoformat()
            }
            
            result = self.client.table('financial_snapshots').insert(snapshot_data).execute()
            
            snapshot_id = result.data[0]['id'] if result.data else None
            logger.info(f"Stored financial snapshot for {company_profile} (ID: {snapshot_id})")
            
            return snapshot_id
            
        except Exception as e:
            logger.error(f"Error storing financial snapshot: {e}")
            raise
    
    async def get_financial_snapshots(
        self,
        company_profile: Optional[str] = None,
        scenario: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get financial snapshots"""
        self.ensure_initialized()
        
        try:
            query = self.client.table('financial_snapshots').select('*')
            
            if company_profile:
                query = query.eq('company_profile', company_profile)
            
            if scenario:
                query = query.eq('scenario', scenario)
            
            result = query.order('captured_at', desc=True).limit(limit).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting financial snapshots: {e}")
            raise
    
    # Customer Intelligence Data
    async def store_customer_insight(
        self,
        insight_type: str,
        customer_data: Dict[str, Any],
        risk_score: Optional[float] = None,
        action_taken: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store customer intelligence insight"""
        self.ensure_initialized()
        
        try:
            insight_data = {
                'insight_type': insight_type,
                'customer_data': customer_data,
                'risk_score': risk_score,
                'action_taken': action_taken,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat()
            }
            
            result = self.client.table('customer_insights').insert(insight_data).execute()
            
            insight_id = result.data[0]['id'] if result.data else None
            logger.info(f"Stored customer insight: {insight_type} (ID: {insight_id})")
            
            return insight_id
            
        except Exception as e:
            logger.error(f"Error storing customer insight: {e}")
            raise
    
    # Market Intelligence Data
    async def store_market_insight(
        self,
        insight_type: str,
        market_data: Dict[str, Any],
        opportunity_score: Optional[float] = None,
        threat_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store market intelligence insight"""
        self.ensure_initialized()
        
        try:
            insight_data = {
                'insight_type': insight_type,
                'market_data': market_data,
                'opportunity_score': opportunity_score,
                'threat_score': threat_score,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat()
            }
            
            result = self.client.table('market_insights').insert(insight_data).execute()
            
            insight_id = result.data[0]['id'] if result.data else None
            logger.info(f"Stored market insight: {insight_type} (ID: {insight_id})")
            
            return insight_id
            
        except Exception as e:
            logger.error(f"Error storing market insight: {e}")
            raise
    
    # Technology Intelligence Data
    async def store_technology_insight(
        self,
        insight_type: str,
        tech_data: Dict[str, Any],
        impact_score: Optional[float] = None,
        adoption_trend: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store technology intelligence insight"""
        self.ensure_initialized()
        
        try:
            insight_data = {
                'insight_type': insight_type,
                'tech_data': tech_data,
                'impact_score': impact_score,
                'adoption_trend': adoption_trend,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat()
            }
            
            result = self.client.table('technology_insights').insert(insight_data).execute()
            
            insight_id = result.data[0]['id'] if result.data else None
            logger.info(f"Stored technology insight: {insight_type} (ID: {insight_id})")
            
            return insight_id
            
        except Exception as e:
            logger.error(f"Error storing technology insight: {e}")
            raise
    
    # System Health & Status
    async def update_system_status(
        self,
        component: str,
        status: str,
        health_score: Optional[float] = None,
        last_error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Update system component status"""
        self.ensure_initialized()
        
        try:
            status_data = {
                'component': component,
                'status': status,
                'health_score': health_score,
                'last_error': last_error,
                'metadata': metadata or {},
                'updated_at': datetime.now().isoformat()
            }
            
            # Upsert based on component name
            result = self.client.table('system_status').upsert(
                status_data,
                on_conflict='component'
            ).execute()
            
            logger.debug(f"Updated system status for {component}: {status}")
            
            return result.data[0]['id'] if result.data else None
            
        except Exception as e:
            logger.error(f"Error updating system status: {e}")
            raise
    
    async def get_system_status(self, component: Optional[str] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Get system status"""
        self.ensure_initialized()
        
        try:
            query = self.client.table('system_status').select('*')
            
            if component:
                result = query.eq('component', component).single().execute()
                return result.data if result.data else {}
            else:
                result = query.order('updated_at', desc=True).execute()
                return result.data or []
                
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            raise
    
    # Analytics & Reporting
    async def get_decision_analytics(
        self,
        hours_back: int = 168  # 1 week
    ) -> Dict[str, Any]:
        """Get AI decision analytics"""
        self.ensure_initialized()
        
        try:
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            cutoff_time_str = cutoff_time.isoformat()
            
            # Get decision counts by type
            decisions = await self.get_decision_history(
                limit=1000,
                min_confidence=0.0
            )
            
            # Filter by time (handle timezone issues)
            recent_decisions = []
            for d in decisions:
                try:
                    created_at = datetime.fromisoformat(d['created_at'].replace('Z', '+00:00'))
                    if created_at.replace(tzinfo=None) >= cutoff_time:
                        recent_decisions.append(d)
                except Exception:
                    # If datetime parsing fails, include the decision
                    recent_decisions.append(d)
            
            # Calculate analytics
            analytics = {
                'total_decisions': len(recent_decisions),
                'avg_confidence': sum(d['confidence'] for d in recent_decisions) / len(recent_decisions) if recent_decisions else 0,
                'decision_types': {},
                'high_confidence_decisions': len([d for d in recent_decisions if d['confidence'] > 0.8]),
                'success_rate': len([d for d in recent_decisions if d.get('outcome') == 'success']) / len(recent_decisions) if recent_decisions else 0,
                'time_range_hours': hours_back
            }
            
            # Count by decision type
            for decision in recent_decisions:
                decision_type = decision['decision_type']
                if decision_type not in analytics['decision_types']:
                    analytics['decision_types'][decision_type] = 0
                analytics['decision_types'][decision_type] += 1
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting decision analytics: {e}")
            raise
    
    # Cleanup and maintenance
    async def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old data to maintain performance"""
        self.ensure_initialized()
        
        try:
            cutoff_date = datetime.now().replace(microsecond=0)
            cutoff_date = cutoff_date.replace(day=cutoff_date.day - days_to_keep)
            cutoff_iso = cutoff_date.isoformat()
            
            # Tables to clean up with their date columns
            cleanup_tables = {
                'performance_metrics': 'timestamp',
                'business_events': 'created_at',
                'financial_snapshots': 'captured_at'
            }
            
            cleanup_summary = {}
            
            for table, date_column in cleanup_tables.items():
                result = self.client.table(table).delete().lt(date_column, cutoff_iso).execute()
                cleanup_summary[table] = len(result.data) if result.data else 0
            
            logger.info(f"Cleanup completed: {cleanup_summary}")
            return cleanup_summary
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            raise


# Global Supabase client instance
supabase_client = SupabaseClient()