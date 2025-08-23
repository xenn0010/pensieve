"""
Enhanced Data Storage Manager for Pensieve
Captures and stores all API calls, search results, and research data
"""

import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

from config.settings import settings
from config.supabase_client import supabase_client
from config.logging_config import get_component_logger

logger = get_component_logger("data_storage_manager")


class SearchType(Enum):
    COMPANY = "company"
    PERSON = "person"
    TECHNOLOGY = "technology"
    MARKET = "market"
    FINANCIAL = "financial"


class ResearchType(Enum):
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    MARKET_RESEARCH = "market_research"
    DUE_DILIGENCE = "due_diligence"
    FINANCIAL_ANALYSIS = "financial_analysis"
    TECHNOLOGY_ASSESSMENT = "technology_assessment"


@dataclass
class APICallMetadata:
    """Metadata for API call tracking"""
    provider: str
    endpoint: str
    method: str = "GET"
    triggered_by: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None


@dataclass
class SearchResult:
    """Structured search result"""
    query: str
    search_type: SearchType
    results_data: Dict[str, Any]
    confidence_score: float
    data_sources: List[str]
    total_results: int = 0


class DataStorageManager:
    """Manages comprehensive data storage for all Pensieve operations"""
    
    def __init__(self):
        self.logger = get_component_logger("data_storage_manager")
        self._active_sessions = {}
    
    async def store_api_call_result(
        self,
        metadata: APICallMetadata,
        request_params: Dict[str, Any],
        response_status: int,
        response_body: Dict[str, Any],
        duration_ms: Optional[int] = None,
        request_headers: Optional[Dict[str, str]] = None,
        response_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """Store API call result with full details"""
        
        try:
            # Calculate response size
            response_size = len(json.dumps(response_body).encode('utf-8'))
            
            # Extract entities from response for better searchability
            extracted_companies = self._extract_companies(response_body)
            extracted_people = self._extract_people(response_body)
            extracted_technologies = self._extract_technologies(response_body)
            extracted_metrics = self._extract_metrics(response_body)
            
            # Store in database
            result = await supabase_client.client.table('api_call_results').insert({
                'api_provider': metadata.provider,
                'endpoint': metadata.endpoint,
                'method': metadata.method,
                'request_params': request_params,
                'request_headers': request_headers or {},
                'response_status': response_status,
                'response_headers': response_headers or {},
                'response_body': response_body,
                'response_size_bytes': response_size,
                'request_timestamp': datetime.now().isoformat(),
                'response_timestamp': datetime.now().isoformat(),
                'duration_ms': duration_ms,
                'triggered_by': metadata.triggered_by,
                'session_id': metadata.session_id,
                'user_id': metadata.user_id,
                'processing_status': 'raw',
                'extracted_companies': extracted_companies,
                'extracted_people': extracted_people,
                'extracted_technologies': extracted_technologies,
                'extracted_metrics': extracted_metrics
            }).execute()
            
            api_call_id = result.data[0]['id']
            
            self.logger.info(f"Stored API call result: {metadata.provider}/{metadata.endpoint} -> {api_call_id}")
            
            # Trigger background processing
            await self._process_api_response_async(api_call_id, response_body, metadata)
            
            return api_call_id
            
        except Exception as e:
            self.logger.error(f"Failed to store API call result: {e}")
            raise
    
    async def store_search_result(
        self,
        search_result: SearchResult,
        api_call_ids: Optional[List[str]] = None,
        session_id: Optional[str] = None,
        requested_by: Optional[str] = None,
        processing_duration_ms: Optional[int] = None
    ) -> str:
        """Store structured search result"""
        
        try:
            # Calculate data freshness and quality scores
            data_freshness_hours = self._calculate_data_freshness(search_result.results_data)
            quality_score = self._calculate_quality_score(search_result.results_data)
            
            # Categorize results
            result_categories = self._categorize_results(search_result.results_data)
            tags = self._generate_tags(search_result.query, search_result.results_data)
            
            # Set expiration based on search type
            expires_at = self._calculate_expiration(search_result.search_type)
            
            result = await supabase_client.client.table('search_results').insert({
                'search_query': search_result.query,
                'search_type': search_result.search_type.value,
                'search_scope': 'comprehensive',  # Default scope
                'total_results': search_result.total_results,
                'results_data': search_result.results_data,
                'confidence_score': search_result.confidence_score,
                'data_sources': search_result.data_sources,
                'api_call_ids': api_call_ids or [],
                'search_timestamp': datetime.now().isoformat(),
                'processing_duration_ms': processing_duration_ms,
                'data_freshness_hours': data_freshness_hours,
                'quality_score': quality_score,
                'requested_by': requested_by,
                'session_id': session_id,
                'result_categories': result_categories,
                'tags': tags,
                'access_count': 0,
                'expires_at': expires_at.isoformat()
            }).execute()
            
            search_result_id = result.data[0]['id']
            
            self.logger.info(f"Stored search result: {search_result.query} -> {search_result_id}")
            
            # Update or create company profile if this is a company search
            if search_result.search_type == SearchType.COMPANY:
                await self._update_company_profile(search_result, search_result_id)
            
            return search_result_id
            
        except Exception as e:
            self.logger.error(f"Failed to store search result: {e}")
            raise
    
    async def create_research_session(
        self,
        objective: str,
        research_type: ResearchType,
        target_companies: Optional[List[str]] = None,
        target_people: Optional[List[str]] = None,
        target_markets: Optional[List[str]] = None,
        research_questions: Optional[List[str]] = None,
        initiated_by: str = "unknown",
        automation_level: str = "manual"
    ) -> str:
        """Create a new research session"""
        
        try:
            session_id = str(uuid.uuid4())
            
            result = await supabase_client.client.table('research_sessions').insert({
                'id': session_id,
                'session_name': f"{research_type.value}_{datetime.now().strftime('%Y%m%d_%H%M')}",
                'research_objective': objective,
                'research_type': research_type.value,
                'target_companies': target_companies or [],
                'target_people': target_people or [],
                'target_markets': target_markets or [],
                'research_questions': research_questions or [],
                'started_at': datetime.now().isoformat(),
                'status': 'active',
                'initiated_by': initiated_by,
                'automation_level': automation_level,
                'search_result_ids': [],
                'api_call_ids': [],
                'intelligence_cache_ids': [],
                'total_api_calls': 0
            }).execute()
            
            self._active_sessions[session_id] = {
                'started_at': time.time(),
                'api_calls': [],
                'search_results': []
            }
            
            self.logger.info(f"Created research session: {objective} -> {session_id}")
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to create research session: {e}")
            raise
    
    async def update_research_session(
        self,
        session_id: str,
        key_findings: Optional[Dict[str, Any]] = None,
        data_summary: Optional[Dict[str, Any]] = None,
        confidence_assessment: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
        api_call_ids: Optional[List[str]] = None,
        search_result_ids: Optional[List[str]] = None
    ):
        """Update research session with new findings and data"""
        
        try:
            update_data = {}
            
            if key_findings:
                update_data['key_findings'] = key_findings
            if data_summary:
                update_data['data_summary'] = data_summary
            if confidence_assessment:
                update_data['confidence_assessment'] = confidence_assessment
            if status:
                update_data['status'] = status
                if status in ['completed', 'failed']:
                    update_data['completed_at'] = datetime.now().isoformat()
            
            # Append new IDs to existing arrays
            if api_call_ids:
                # Get current session
                current = await supabase_client.client.table('research_sessions').select('api_call_ids, total_api_calls').eq('id', session_id).execute()
                if current.data:
                    existing_api_calls = current.data[0].get('api_call_ids', [])
                    existing_api_calls.extend(api_call_ids)
                    update_data['api_call_ids'] = existing_api_calls
                    update_data['total_api_calls'] = len(existing_api_calls)
            
            if search_result_ids:
                current = await supabase_client.client.table('research_sessions').select('search_result_ids').eq('id', session_id).execute()
                if current.data:
                    existing_search_results = current.data[0].get('search_result_ids', [])
                    existing_search_results.extend(search_result_ids)
                    update_data['search_result_ids'] = existing_search_results
            
            if update_data:
                await supabase_client.client.table('research_sessions').update(update_data).eq('id', session_id).execute()
                self.logger.info(f"Updated research session: {session_id}")
                
        except Exception as e:
            self.logger.error(f"Failed to update research session {session_id}: {e}")
            raise
    
    async def get_company_research_data(self, company_name: str) -> Dict[str, Any]:
        """Get comprehensive research data for a company"""
        
        try:
            # Use the database function to get aggregated data
            result = await supabase_client.client.rpc('get_company_research_data', {
                'p_company_name': company_name
            }).execute()
            
            if result.data:
                return result.data
            else:
                return {'profile': None, 'recent_searches': [], 'research_sessions': [], 'intelligence_findings': [], 'cached_intelligence': []}
                
        except Exception as e:
            self.logger.error(f"Failed to get company research data for {company_name}: {e}")
            return {}
    
    async def store_intelligence_finding(
        self,
        finding_type: str,
        title: str,
        description: str,
        confidence_level: str,
        related_companies: Optional[List[str]] = None,
        key_metrics: Optional[Dict[str, Any]] = None,
        supporting_evidence: Optional[Dict[str, Any]] = None,
        urgency_level: str = "medium",
        discovered_by: str = "autonomous_agent",
        source_api_calls: Optional[List[str]] = None
    ) -> str:
        """Store an intelligence finding"""
        
        try:
            result = await supabase_client.client.table('intelligence_findings').insert({
                'finding_type': finding_type,
                'confidence_level': confidence_level,
                'title': title,
                'description': description,
                'key_metrics': key_metrics or {},
                'supporting_evidence': supporting_evidence or {},
                'related_companies': related_companies or [],
                'urgency_level': urgency_level,
                'source_api_calls': source_api_calls or [],
                'discovered_at': datetime.now().isoformat(),
                'discovered_by': discovered_by,
                'processing_method': 'autonomous_analysis',
                'validation_status': 'unvalidated'
            }).execute()
            
            finding_id = result.data[0]['id']
            self.logger.info(f"Stored intelligence finding: {title} -> {finding_id}")
            
            return finding_id
            
        except Exception as e:
            self.logger.error(f"Failed to store intelligence finding: {e}")
            raise
    
    # Helper methods for data processing
    
    def _extract_companies(self, data: Dict[str, Any]) -> List[str]:
        """Extract company names from API response"""
        companies = []
        
        # Convert to string and look for common company patterns
        data_str = json.dumps(data).lower()
        
        # Simple heuristics - in production, use NLP/NER
        import re
        
        # Look for common company patterns
        company_patterns = [
            r'\b(\w+\s+(?:inc|corp|llc|ltd|gmbh))\b',
            r'\b(\w+\s+(?:technologies|tech|systems|software))\b'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, data_str)
            companies.extend([match.title() for match in matches])
        
        return list(set(companies))[:10]  # Limit to 10
    
    def _extract_people(self, data: Dict[str, Any]) -> List[str]:
        """Extract people names from API response"""
        # Simple extraction - in production, use NLP/NER
        return []
    
    def _extract_technologies(self, data: Dict[str, Any]) -> List[str]:
        """Extract technology names from API response"""
        technologies = []
        
        # Look for common technology keywords
        data_str = json.dumps(data).lower()
        tech_keywords = [
            'python', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'mongodb',
            'postgresql', 'redis', 'elasticsearch', 'tensorflow', 'pytorch'
        ]
        
        for tech in tech_keywords:
            if tech in data_str:
                technologies.append(tech)
        
        return technologies
    
    def _extract_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract numerical metrics from API response"""
        metrics = {}
        
        # Look for common metric patterns
        def find_numbers(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, (int, float)) and key.lower() in [
                        'revenue', 'employees', 'funding', 'valuation', 'growth_rate',
                        'burn_rate', 'runway', 'customers', 'users'
                    ]:
                        metrics[f"{path}.{key}" if path else key] = value
                    elif isinstance(value, (dict, list)):
                        find_numbers(value, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        find_numbers(item, f"{path}[{i}]" if path else f"[{i}]")
        
        find_numbers(data)
        return metrics
    
    def _calculate_data_freshness(self, data: Dict[str, Any]) -> float:
        """Calculate how fresh the data is in hours"""
        # Simple heuristic - in production, look for timestamps in data
        return 1.0  # Assume 1 hour fresh
    
    def _calculate_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate data quality score 0-1"""
        # Simple scoring based on data completeness
        if not data:
            return 0.0
        
        score = 0.5  # Base score
        
        # Add points for data richness
        if len(str(data)) > 1000:  # Substantial data
            score += 0.2
        if isinstance(data, dict) and len(data) > 5:  # Multiple fields
            score += 0.2
        if any(isinstance(v, list) for v in data.values() if isinstance(data, dict)):  # Arrays present
            score += 0.1
        
        return min(score, 1.0)
    
    def _categorize_results(self, data: Dict[str, Any]) -> List[str]:
        """Categorize results based on content"""
        categories = []
        
        data_str = json.dumps(data).lower()
        
        category_keywords = {
            'financial_health': ['revenue', 'funding', 'cash', 'burn', 'runway', 'financial'],
            'competitive_intel': ['competitor', 'market_share', 'position', 'competitive'],
            'market_trends': ['trend', 'growth', 'market', 'industry'],
            'technology_stack': ['technology', 'tech', 'software', 'platform'],
            'team_info': ['employee', 'team', 'hiring', 'personnel']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in data_str for keyword in keywords):
                categories.append(category)
        
        return categories
    
    def _generate_tags(self, query: str, data: Dict[str, Any]) -> List[str]:
        """Generate tags for search results"""
        tags = []
        
        # Add query words as tags
        query_words = query.lower().split()
        tags.extend([word for word in query_words if len(word) > 3])
        
        # Add content-based tags
        data_str = json.dumps(data).lower()
        
        if 'startup' in data_str or 'seed' in data_str:
            tags.append('startup')
        if 'enterprise' in data_str or 'corporation' in data_str:
            tags.append('enterprise')
        if 'public' in data_str or 'nasdaq' in data_str:
            tags.append('public_company')
        
        return list(set(tags))[:10]  # Limit to 10 unique tags
    
    def _calculate_expiration(self, search_type: SearchType) -> datetime:
        """Calculate when search results should expire"""
        
        expiration_hours = {
            SearchType.COMPANY: 24,      # Company data expires in 1 day
            SearchType.FINANCIAL: 6,     # Financial data expires in 6 hours
            SearchType.MARKET: 12,       # Market data expires in 12 hours
            SearchType.TECHNOLOGY: 48,   # Technology data expires in 2 days
            SearchType.PERSON: 168       # Person data expires in 1 week
        }
        
        hours = expiration_hours.get(search_type, 24)
        return datetime.now() + timedelta(hours=hours)
    
    async def _update_company_profile(self, search_result: SearchResult, search_result_id: str):
        """Update or create company profile from search result"""
        
        try:
            # Extract company name from query
            company_name = search_result.query.strip()
            
            # Try to extract structured data
            profile_data = {
                'company_name': company_name,
                'data_sources': search_result.data_sources,
                'last_updated_at': datetime.now().isoformat(),
                'data_quality_score': search_result.confidence_score,
                'related_search_results': [search_result_id],
                'times_researched': 1,
                'last_researched_at': datetime.now().isoformat()
            }
            
            # Extract additional data from results
            if isinstance(search_result.results_data, dict):
                if 'industry' in search_result.results_data:
                    profile_data['industry'] = search_result.results_data['industry']
                if 'financial_metrics' in search_result.results_data:
                    profile_data['financial_metrics'] = search_result.results_data['financial_metrics']
                if 'employee_metrics' in search_result.results_data:
                    profile_data['employee_metrics'] = search_result.results_data['employee_metrics']
            
            # Upsert company profile
            await supabase_client.client.table('company_profiles').upsert(
                profile_data,
                on_conflict='company_name'
            ).execute()
            
            self.logger.info(f"Updated company profile for: {company_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to update company profile: {e}")
    
    async def _process_api_response_async(self, api_call_id: str, response_body: Dict[str, Any], metadata: APICallMetadata):
        """Background processing of API responses"""
        
        try:
            # Mark as being processed
            await supabase_client.client.table('api_call_results').update({
                'processing_status': 'processing'
            }).eq('id', api_call_id).execute()
            
            # Extract insights and create intelligence findings
            insights = await self._extract_insights_from_response(response_body, metadata)
            
            for insight in insights:
                await self.store_intelligence_finding(
                    finding_type=insight['type'],
                    title=insight['title'],
                    description=insight['description'],
                    confidence_level=insight['confidence'],
                    related_companies=insight.get('companies', []),
                    key_metrics=insight.get('metrics', {}),
                    source_api_calls=[api_call_id]
                )
            
            # Mark as processed
            await supabase_client.client.table('api_call_results').update({
                'processing_status': 'processed'
            }).eq('id', api_call_id).execute()
            
        except Exception as e:
            # Mark as failed
            await supabase_client.client.table('api_call_results').update({
                'processing_status': 'failed',
                'error_message': str(e)
            }).eq('id', api_call_id).execute()
            
            self.logger.error(f"Failed to process API response {api_call_id}: {e}")
    
    async def _extract_insights_from_response(self, response_body: Dict[str, Any], metadata: APICallMetadata) -> List[Dict[str, Any]]:
        """Extract actionable insights from API response"""
        
        insights = []
        
        # Simple insight extraction - in production, use more sophisticated analysis
        if metadata.provider == 'sixtyfour':
            # Look for financial health indicators
            if 'financial_health' in response_body:
                insights.append({
                    'type': 'financial_trend',
                    'title': 'Financial Health Update',
                    'description': f"New financial data available for analysis",
                    'confidence': 'medium',
                    'companies': self._extract_companies(response_body),
                    'metrics': self._extract_metrics(response_body)
                })
        
        return insights


# Global instance
data_storage_manager = DataStorageManager()
