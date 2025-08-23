import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

import httpx
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
import redis.asyncio as redis
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)


class SixtyFourMarketIntelligence:
    def __init__(self):
        self.server = Server("sixtyfour-market-intelligence")
        self.http_client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {settings.sixtyfour_api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )
        self.redis_client = None
        self.monitoring_active = False
        
    async def initialize(self):
        """Initialize connections and setup MCP server"""
        try:
            self.redis_client = redis.from_url(settings.redis_url)
            await self._setup_mcp_resources()
            await self._setup_mcp_tools()
            logger.info("SixtyFour market intelligence initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SixtyFour market intelligence: {e}")
            raise
        
    async def _setup_mcp_resources(self):
        """Setup MCP resources for market intelligence"""
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            return [
                Resource(
                    uri="sixtyfour://competitors/analysis",
                    name="Competitor Intelligence Analysis",
                    mimeType="application/json",
                    description="Deep competitive landscape analysis and threat assessment"
                ),
                Resource(
                    uri="sixtyfour://market/opportunities",
                    name="Market Opportunities",
                    mimeType="application/json",
                    description="Identified market gaps and expansion opportunities"
                ),
                Resource(
                    uri="sixtyfour://leads/enrichment", 
                    name="Lead Intelligence & Enrichment",
                    mimeType="application/json",
                    description="Enriched lead data with market intelligence"
                ),
                Resource(
                    uri="sixtyfour://industry/trends",
                    name="Industry Trend Analysis",
                    mimeType="application/json",
                    description="Real-time industry trends and market movement analysis"
                ),
                Resource(
                    uri="sixtyfour://positioning/analysis",
                    name="Market Positioning Analysis",
                    mimeType="application/json",
                    description="Competitive positioning and market share analysis"
                )
            ]
            
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            try:
                if uri == "sixtyfour://competitors/analysis":
                    data = await self._analyze_competitors()
                elif uri == "sixtyfour://market/opportunities":
                    data = await self._identify_market_opportunities()
                elif uri == "sixtyfour://leads/enrichment":
                    data = await self._enrich_leads_data()
                elif uri == "sixtyfour://industry/trends":
                    data = await self._analyze_industry_trends()
                elif uri == "sixtyfour://positioning/analysis":
                    data = await self._analyze_market_positioning()
                else:
                    raise ValueError(f"Unknown resource: {uri}")
                return json.dumps(data, indent=2)
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                return json.dumps({"error": str(e)}, indent=2)
    
    async def _setup_mcp_tools(self):
        """Setup MCP tools for market intelligence actions"""
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="launch_competitive_research",
                    description="Launch deep competitive research on specific companies or market segments",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target_companies": {"type": "array", "items": {"type": "string"}},
                            "research_depth": {"type": "string", "enum": ["basic", "comprehensive", "deep_dive"]},
                            "focus_areas": {"type": "array", "items": {"type": "string"}},
                            "urgency": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
                        },
                        "required": ["target_companies", "research_depth"]
                    }
                ),
                Tool(
                    name="monitor_competitor_activity",
                    description="Set up automated monitoring for competitor activities and changes",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "competitor_domains": {"type": "array", "items": {"type": "string"}},
                            "monitoring_frequency": {"type": "string", "enum": ["hourly", "daily", "weekly"]},
                            "alert_triggers": {"type": "array", "items": {"type": "string"}},
                            "notification_channels": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["competitor_domains", "monitoring_frequency"]
                    }
                ),
                Tool(
                    name="generate_market_report",
                    description="Generate comprehensive market intelligence report",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "report_type": {"type": "string", "enum": ["competitive_landscape", "market_opportunity", "industry_analysis", "positioning_report"]},
                            "time_horizon": {"type": "string", "enum": ["current", "3_months", "6_months", "1_year"]},
                            "target_audience": {"type": "string", "enum": ["executives", "sales_team", "product_team", "investors"]},
                            "include_recommendations": {"type": "boolean", "default": True}
                        },
                        "required": ["report_type", "target_audience"]
                    }
                ),
                Tool(
                    name="analyze_market_entry",
                    description="Analyze potential market entry opportunities and strategies",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target_markets": {"type": "array", "items": {"type": "string"}},
                            "entry_strategies": {"type": "array", "items": {"type": "string"}},
                            "risk_tolerance": {"type": "string", "enum": ["low", "medium", "high"]},
                            "timeline": {"type": "string", "enum": ["immediate", "3_months", "6_months", "1_year"]}
                        },
                        "required": ["target_markets", "entry_strategies"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            try:
                if name == "launch_competitive_research":
                    result = await self._launch_competitive_research(arguments)
                elif name == "monitor_competitor_activity":
                    result = await self._setup_competitor_monitoring(arguments)
                elif name == "generate_market_report":
                    result = await self._generate_market_report(arguments)
                elif name == "analyze_market_entry":
                    result = await self._analyze_market_entry(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]
    
    async def start_monitoring(self):
        """Start continuous market intelligence monitoring"""
        self.monitoring_active = True
        logger.info("Starting SixtyFour market monitoring")
        
        tasks = [
            asyncio.create_task(self._monitor_competitor_changes()),
            asyncio.create_task(self._monitor_market_opportunities()),
            asyncio.create_task(self._monitor_industry_trends()),
            asyncio.create_task(self._monitor_funding_activities())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error in market monitoring: {e}")
    
    async def _monitor_competitor_changes(self):
        """Monitor competitor activities and changes"""
        while self.monitoring_active:
            try:
                competitor_data = await self._analyze_competitors()
                
                # Check for significant competitor changes
                for competitor in competitor_data.get('competitors', []):
                    threat_score = competitor.get('threat_score', 0)
                    
                    if threat_score > settings.competitor_threat_threshold:
                        await self._publish_market_alert({
                            'alert_type': 'high_competitor_threat',
                            'competitor': competitor['name'],
                            'threat_score': threat_score,
                            'changes': competitor.get('recent_changes', []),
                            'severity': 'high',
                            'data': competitor
                        })
                
                # Check for new market entrants
                new_entrants = competitor_data.get('new_entrants', [])
                if new_entrants:
                    await self._publish_market_alert({
                        'alert_type': 'new_market_entrants',
                        'entrants': new_entrants,
                        'severity': 'medium',
                        'data': {'new_entrants': new_entrants}
                    })
                
                await asyncio.sleep(3600)  # Check every hour
                
            except Exception as e:
                logger.error(f"Error monitoring competitors: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_market_opportunities(self):
        """Monitor for emerging market opportunities"""
        while self.monitoring_active:
            try:
                opportunities = await self._identify_market_opportunities()
                
                # Check for high-value opportunities
                high_value_opportunities = [
                    opp for opp in opportunities.get('opportunities', [])
                    if opp.get('opportunity_score', 0) > 0.8
                ]
                
                if high_value_opportunities:
                    await self._publish_market_alert({
                        'alert_type': 'high_value_opportunities',
                        'opportunity_count': len(high_value_opportunities),
                        'opportunities': high_value_opportunities,
                        'severity': 'high',
                        'data': opportunities
                    })
                
                await asyncio.sleep(7200)  # Check every 2 hours
                
            except Exception as e:
                logger.error(f"Error monitoring opportunities: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_industry_trends(self):
        """Monitor industry trends and disruptions"""
        while self.monitoring_active:
            try:
                trends = await self._analyze_industry_trends()
                
                # Check for disruptive trends
                disruptive_trends = [
                    trend for trend in trends.get('trends', [])
                    if trend.get('disruption_potential', 0) > 0.7
                ]
                
                if disruptive_trends:
                    await self._publish_market_alert({
                        'alert_type': 'disruptive_trends',
                        'trend_count': len(disruptive_trends),
                        'trends': disruptive_trends,
                        'severity': 'medium',
                        'data': trends
                    })
                
                # Check for growth opportunities in trends
                growth_trends = [
                    trend for trend in trends.get('trends', [])
                    if trend.get('growth_potential', 0) > 0.8
                ]
                
                if growth_trends:
                    await self._publish_market_alert({
                        'alert_type': 'growth_trend_opportunities',
                        'trend_count': len(growth_trends),
                        'trends': growth_trends,
                        'severity': 'medium',
                        'data': trends
                    })
                
                await asyncio.sleep(10800)  # Check every 3 hours
                
            except Exception as e:
                logger.error(f"Error monitoring trends: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_funding_activities(self):
        """Monitor funding rounds and investment activities"""
        while self.monitoring_active:
            try:
                funding_data = await self._get_funding_intelligence()
                
                # Check for significant competitor funding
                large_rounds = [
                    round_data for round_data in funding_data.get('recent_rounds', [])
                    if round_data.get('amount', 0) > 10000000  # $10M+
                ]
                
                if large_rounds:
                    await self._publish_market_alert({
                        'alert_type': 'significant_competitor_funding',
                        'round_count': len(large_rounds),
                        'funding_rounds': large_rounds,
                        'severity': 'high',
                        'data': funding_data
                    })
                
                await asyncio.sleep(21600)  # Check every 6 hours
                
            except Exception as e:
                logger.error(f"Error monitoring funding: {e}")
                await asyncio.sleep(300)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _analyze_competitors(self) -> Dict[str, Any]:
        """Analyze competitive landscape using SixtyFour API"""
        try:
            # Get competitor data
            response = await self.http_client.get("/api/v1/competitors/analysis")
            response.raise_for_status()
            data = response.json().get('data', {})
            
            competitors = []
            for competitor_data in data.get('competitors', []):
                competitor_analysis = await self._analyze_single_competitor(competitor_data)
                competitors.append(competitor_analysis)
            
            # Sort by threat score
            competitors.sort(key=lambda x: x.get('threat_score', 0), reverse=True)
            
            return {
                'competitors': competitors,
                'total_competitors': len(competitors),
                'market_concentration': data.get('market_concentration', 0),
                'competitive_intensity': data.get('competitive_intensity', 0),
                'new_entrants': data.get('new_entrants', []),
                'market_leader': competitors[0] if competitors else None,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing competitors: {e}")
            return {'error': str(e)}
    
    async def _analyze_single_competitor(self, competitor_data: Dict) -> Dict[str, Any]:
        """Analyze individual competitor"""
        try:
            # Calculate threat score based on multiple factors
            threat_factors = {
                'market_share': competitor_data.get('market_share', 0) / 100,
                'growth_rate': min(competitor_data.get('growth_rate', 0) / 50, 1.0),
                'funding_amount': min(competitor_data.get('recent_funding', 0) / 50000000, 1.0),
                'feature_overlap': competitor_data.get('feature_similarity', 0) / 100,
                'customer_satisfaction': competitor_data.get('customer_rating', 3) / 5,
                'innovation_score': competitor_data.get('innovation_rating', 0) / 10
            }
            
            # Weighted threat score calculation
            weights = {
                'market_share': 0.25,
                'growth_rate': 0.20,
                'funding_amount': 0.15,
                'feature_overlap': 0.15,
                'customer_satisfaction': 0.15,
                'innovation_score': 0.10
            }
            
            threat_score = sum(
                threat_factors.get(factor, 0) * weight
                for factor, weight in weights.items()
            )
            
            return {
                'name': competitor_data.get('company_name', ''),
                'domain': competitor_data.get('domain', ''),
                'threat_score': min(threat_score, 1.0),
                'threat_level': self._get_threat_level(threat_score),
                'market_share': competitor_data.get('market_share', 0),
                'employee_count': competitor_data.get('employee_count', 0),
                'recent_funding': competitor_data.get('recent_funding', 0),
                'funding_stage': competitor_data.get('funding_stage', ''),
                'growth_indicators': competitor_data.get('growth_metrics', {}),
                'recent_changes': competitor_data.get('recent_activities', []),
                'competitive_advantages': competitor_data.get('key_strengths', []),
                'potential_weaknesses': competitor_data.get('identified_gaps', []),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing competitor: {e}")
            return {'error': str(e)}
    
    def _get_threat_level(self, score: float) -> str:
        """Convert threat score to threat level"""
        if score >= 0.8:
            return 'critical'
        elif score >= 0.6:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _identify_market_opportunities(self) -> Dict[str, Any]:
        """Identify market gaps and opportunities"""
        try:
            response = await self.http_client.get("/api/v1/market/opportunities")
            response.raise_for_status()
            data = response.json().get('data', {})
            
            opportunities = []
            for opp_data in data.get('opportunities', []):
                opportunity = await self._analyze_opportunity(opp_data)
                opportunities.append(opportunity)
            
            # Sort by opportunity score
            opportunities.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
            
            return {
                'opportunities': opportunities,
                'total_opportunities': len(opportunities),
                'high_priority_count': len([o for o in opportunities if o.get('opportunity_score', 0) > 0.7]),
                'market_size_analysis': data.get('total_addressable_market', {}),
                'trend_alignment': data.get('trend_alignment', {}),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error identifying opportunities: {e}")
            return {'error': str(e)}
    
    async def _analyze_opportunity(self, opp_data: Dict) -> Dict[str, Any]:
        """Analyze individual market opportunity"""
        try:
            # Calculate opportunity score
            opportunity_factors = {
                'market_size': min(opp_data.get('market_size_millions', 0) / 1000, 1.0),
                'growth_rate': min(opp_data.get('market_growth_rate', 0) / 30, 1.0),
                'competition_density': 1 - min(opp_data.get('competitor_count', 10) / 20, 1.0),
                'entry_barrier': 1 - (opp_data.get('entry_difficulty', 5) / 10),
                'trend_alignment': opp_data.get('trend_score', 0) / 10,
                'customer_demand': opp_data.get('demand_intensity', 0) / 10
            }
            
            weights = {
                'market_size': 0.25,
                'growth_rate': 0.20,
                'competition_density': 0.15,
                'entry_barrier': 0.15,
                'trend_alignment': 0.15,
                'customer_demand': 0.10
            }
            
            opportunity_score = sum(
                opportunity_factors.get(factor, 0) * weight
                for factor, weight in weights.items()
            )
            
            return {
                'opportunity_id': opp_data.get('id', ''),
                'title': opp_data.get('title', ''),
                'description': opp_data.get('description', ''),
                'opportunity_score': min(opportunity_score, 1.0),
                'priority_level': self._get_priority_level(opportunity_score),
                'market_segment': opp_data.get('market_segment', ''),
                'estimated_market_size': opp_data.get('market_size_millions', 0),
                'growth_potential': opp_data.get('market_growth_rate', 0),
                'competitive_landscape': opp_data.get('competition_analysis', {}),
                'entry_requirements': opp_data.get('entry_requirements', []),
                'timeline_to_market': opp_data.get('development_timeline', ''),
                'risk_factors': opp_data.get('identified_risks', []),
                'success_indicators': opp_data.get('success_metrics', [])
            }
            
        except Exception as e:
            logger.error(f"Error analyzing opportunity: {e}")
            return {'error': str(e)}
    
    def _get_priority_level(self, score: float) -> str:
        """Convert opportunity score to priority level"""
        if score >= 0.8:
            return 'critical'
        elif score >= 0.6:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _enrich_leads_data(self) -> Dict[str, Any]:
        """Enrich lead data with market intelligence"""
        try:
            response = await self.http_client.get("/api/v1/leads/enrichment")
            response.raise_for_status()
            data = response.json().get('data', {})
            
            enriched_leads = []
            for lead_data in data.get('leads', []):
                enriched_lead = await self._enrich_single_lead(lead_data)
                enriched_leads.append(enriched_lead)
            
            return {
                'enriched_leads': enriched_leads,
                'total_leads': len(enriched_leads),
                'high_value_leads': len([l for l in enriched_leads if l.get('value_score', 0) > 0.7]),
                'enrichment_coverage': data.get('enrichment_coverage', 0),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error enriching leads: {e}")
            return {'error': str(e)}
    
    async def _enrich_single_lead(self, lead_data: Dict) -> Dict[str, Any]:
        """Enrich individual lead with market intelligence"""
        try:
            company_domain = lead_data.get('company_domain', '')
            
            # Get company intelligence
            company_intel = await self._get_company_intelligence(company_domain)
            
            # Calculate lead value score
            value_factors = {
                'company_size': min(lead_data.get('employee_count', 0) / 1000, 1.0),
                'revenue_estimate': min(lead_data.get('estimated_revenue', 0) / 100000000, 1.0),
                'growth_indicators': company_intel.get('growth_score', 0) / 10,
                'technology_fit': lead_data.get('tech_stack_match', 0) / 10,
                'buying_intent': lead_data.get('intent_score', 0) / 10,
                'market_segment_fit': lead_data.get('segment_alignment', 0) / 10
            }
            
            weights = {
                'company_size': 0.20,
                'revenue_estimate': 0.20,
                'growth_indicators': 0.15,
                'technology_fit': 0.15,
                'buying_intent': 0.20,
                'market_segment_fit': 0.10
            }
            
            value_score = sum(
                value_factors.get(factor, 0) * weight
                for factor, weight in weights.items()
            )
            
            return {
                'lead_id': lead_data.get('id', ''),
                'company_name': lead_data.get('company_name', ''),
                'company_domain': company_domain,
                'value_score': min(value_score, 1.0),
                'priority_level': self._get_priority_level(value_score),
                'contact_info': lead_data.get('contacts', []),
                'company_intelligence': company_intel,
                'recommended_approach': self._get_sales_approach(lead_data, company_intel),
                'competitive_landscape': company_intel.get('competitor_analysis', {}),
                'market_timing': company_intel.get('market_timing', ''),
                'enrichment_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error enriching lead: {e}")
            return {'error': str(e)}
    
    async def _get_company_intelligence(self, domain: str) -> Dict[str, Any]:
        """Get detailed company intelligence"""
        try:
            if not domain:
                return {}
                
            response = await self.http_client.get(f"/api/v1/companies/{domain}/intelligence")
            response.raise_for_status()
            return response.json().get('data', {})
        except Exception as e:
            logger.error(f"Error getting company intelligence for {domain}: {e}")
            return {}
    
    def _get_sales_approach(self, lead_data: Dict, company_intel: Dict) -> Dict[str, str]:
        """Generate recommended sales approach"""
        company_stage = company_intel.get('funding_stage', 'unknown')
        pain_points = company_intel.get('identified_challenges', [])
        tech_stack = lead_data.get('technology_stack', [])
        
        approach_strategies = {
            'seed': 'Focus on ROI and quick implementation',
            'series_a': 'Emphasize scalability and growth enablement',
            'series_b': 'Highlight enterprise features and security',
            'growth': 'Position as strategic competitive advantage',
            'unknown': 'Discovery-focused approach to understand needs'
        }
        
        return {
            'primary_strategy': approach_strategies.get(company_stage, approach_strategies['unknown']),
            'key_pain_points': pain_points[:3],  # Top 3 pain points
            'technical_fit': f"High compatibility with {', '.join(tech_stack[:3])}" if tech_stack else "Technical assessment needed",
            'timing_indicators': company_intel.get('buying_signals', [])
        }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _analyze_industry_trends(self) -> Dict[str, Any]:
        """Analyze industry trends and disruptions"""
        try:
            response = await self.http_client.get("/api/v1/industry/trends")
            response.raise_for_status()
            data = response.json().get('data', {})
            
            trends = []
            for trend_data in data.get('trends', []):
                trend_analysis = await self._analyze_single_trend(trend_data)
                trends.append(trend_analysis)
            
            return {
                'trends': trends,
                'trend_summary': data.get('summary', {}),
                'disruptive_technologies': data.get('disruptive_tech', []),
                'market_shifts': data.get('market_changes', []),
                'investment_patterns': data.get('funding_trends', {}),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {'error': str(e)}
    
    async def _analyze_single_trend(self, trend_data: Dict) -> Dict[str, Any]:
        """Analyze individual industry trend"""
        try:
            # Calculate impact scores
            disruption_potential = min(trend_data.get('disruption_score', 0) / 10, 1.0)
            growth_potential = min(trend_data.get('growth_score', 0) / 10, 1.0)
            adoption_rate = min(trend_data.get('adoption_rate', 0) / 100, 1.0)
            
            return {
                'trend_id': trend_data.get('id', ''),
                'title': trend_data.get('title', ''),
                'description': trend_data.get('description', ''),
                'category': trend_data.get('category', ''),
                'disruption_potential': disruption_potential,
                'growth_potential': growth_potential,
                'adoption_rate': adoption_rate,
                'time_horizon': trend_data.get('maturity_timeline', ''),
                'key_players': trend_data.get('leading_companies', []),
                'market_impact': trend_data.get('market_implications', []),
                'opportunities': trend_data.get('business_opportunities', []),
                'threats': trend_data.get('potential_risks', []),
                'investment_activity': trend_data.get('funding_activity', {}),
                'geographic_adoption': trend_data.get('regional_data', {})
            }
            
        except Exception as e:
            logger.error(f"Error analyzing trend: {e}")
            return {'error': str(e)}
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _analyze_market_positioning(self) -> Dict[str, Any]:
        """Analyze competitive positioning and market share"""
        try:
            response = await self.http_client.get("/api/v1/market/positioning")
            response.raise_for_status()
            data = response.json().get('data', {})
            
            return {
                'market_map': data.get('competitive_landscape', {}),
                'positioning_analysis': data.get('positioning_matrix', {}),
                'market_share_distribution': data.get('market_shares', {}),
                'competitive_gaps': data.get('market_gaps', []),
                'positioning_recommendations': data.get('recommendations', []),
                'differentiation_opportunities': data.get('differentiation_areas', []),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing positioning: {e}")
            return {'error': str(e)}
    
    async def _get_funding_intelligence(self) -> Dict[str, Any]:
        """Get funding and investment intelligence"""
        try:
            response = await self.http_client.get("/api/v1/funding/intelligence")
            response.raise_for_status()
            data = response.json().get('data', {})
            
            return {
                'recent_rounds': data.get('funding_rounds', []),
                'investment_trends': data.get('market_trends', {}),
                'investor_activity': data.get('investor_insights', {}),
                'valuation_trends': data.get('valuation_analysis', {}),
                'market_sentiment': data.get('investment_sentiment', {}),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting funding intelligence: {e}")
            return {'error': str(e)}
    
    async def _launch_competitive_research(self, args: Dict) -> Dict[str, Any]:
        """Launch deep competitive research"""
        try:
            target_companies = args['target_companies']
            research_depth = args['research_depth']
            focus_areas = args.get('focus_areas', [])
            urgency = args.get('urgency', 'medium')
            
            research_data = {
                'targets': target_companies,
                'depth': research_depth,
                'focus_areas': focus_areas,
                'urgency': urgency,
                'initiated_at': datetime.now().isoformat(),
                'initiated_by': 'pensieve_cio'
            }
            
            # Launch research via SixtyFour API
            response = await self.http_client.post(
                "/api/v1/research/competitive",
                json=research_data
            )
            response.raise_for_status()
            
            return {
                'research_id': response.json().get('id'),
                'target_companies': target_companies,
                'research_depth': research_depth,
                'estimated_completion': response.json().get('estimated_completion'),
                'status': 'initiated',
                'tracking_url': response.json().get('tracking_url')
            }
            
        except Exception as e:
            logger.error(f"Error launching competitive research: {e}")
            return {'error': str(e)}
    
    async def _setup_competitor_monitoring(self, args: Dict) -> Dict[str, Any]:
        """Setup automated competitor monitoring"""
        try:
            competitor_domains = args['competitor_domains']
            frequency = args['monitoring_frequency']
            triggers = args.get('alert_triggers', [])
            channels = args.get('notification_channels', [])
            
            monitoring_config = {
                'domains': competitor_domains,
                'frequency': frequency,
                'triggers': triggers,
                'notification_channels': channels,
                'created_at': datetime.now().isoformat(),
                'created_by': 'pensieve_cio'
            }
            
            # Setup monitoring via SixtyFour API
            response = await self.http_client.post(
                "/api/v1/monitoring/competitors",
                json=monitoring_config
            )
            response.raise_for_status()
            
            return {
                'monitoring_id': response.json().get('id'),
                'monitored_domains': competitor_domains,
                'frequency': frequency,
                'active_triggers': len(triggers),
                'status': 'active',
                'next_check': response.json().get('next_scheduled_check')
            }
            
        except Exception as e:
            logger.error(f"Error setting up monitoring: {e}")
            return {'error': str(e)}
    
    async def _generate_market_report(self, args: Dict) -> Dict[str, Any]:
        """Generate comprehensive market intelligence report"""
        try:
            report_type = args['report_type']
            target_audience = args['target_audience']
            time_horizon = args.get('time_horizon', 'current')
            include_recommendations = args.get('include_recommendations', True)
            
            report_config = {
                'type': report_type,
                'audience': target_audience,
                'time_horizon': time_horizon,
                'include_recommendations': include_recommendations,
                'requested_at': datetime.now().isoformat(),
                'requested_by': 'pensieve_cio'
            }
            
            # Generate report via SixtyFour API
            response = await self.http_client.post(
                "/api/v1/reports/generate",
                json=report_config
            )
            response.raise_for_status()
            
            return {
                'report_id': response.json().get('id'),
                'report_type': report_type,
                'target_audience': target_audience,
                'estimated_completion': response.json().get('estimated_completion'),
                'status': 'generating',
                'download_url': response.json().get('download_url')
            }
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {'error': str(e)}
    
    async def _analyze_market_entry(self, args: Dict) -> Dict[str, Any]:
        """Analyze market entry opportunities"""
        try:
            target_markets = args['target_markets']
            entry_strategies = args['entry_strategies']
            risk_tolerance = args.get('risk_tolerance', 'medium')
            timeline = args.get('timeline', '6_months')
            
            analysis_config = {
                'target_markets': target_markets,
                'strategies': entry_strategies,
                'risk_tolerance': risk_tolerance,
                'timeline': timeline,
                'analysis_date': datetime.now().isoformat()
            }
            
            # Analyze via SixtyFour API
            response = await self.http_client.post(
                "/api/v1/analysis/market-entry",
                json=analysis_config
            )
            response.raise_for_status()
            
            return {
                'analysis_id': response.json().get('id'),
                'target_markets': target_markets,
                'recommended_strategies': response.json().get('recommended_strategies', []),
                'risk_assessment': response.json().get('risk_analysis', {}),
                'market_readiness': response.json().get('readiness_score', 0),
                'entry_timeline': response.json().get('recommended_timeline'),
                'investment_requirements': response.json().get('investment_estimate', {})
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market entry: {e}")
            return {'error': str(e)}
    
    async def _publish_market_alert(self, alert_data: Dict):
        """Publish market alert to Redis stream"""
        try:
            await self.redis_client.xadd(
                'sixtyfour_events',
                {
                    'data': json.dumps(alert_data),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'sixtyfour_market_intelligence'
                }
            )
            logger.info(f"Published market alert: {alert_data['alert_type']}")
        except Exception as e:
            logger.error(f"Error publishing market alert: {e}")