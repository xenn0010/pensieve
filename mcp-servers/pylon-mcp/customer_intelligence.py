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


class PylonCustomerIntelligence:
    def __init__(self):
        self.server = Server("pylon-customer-intelligence")
        self.http_client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {settings.pylon_api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        self.redis_client = None
        self.monitoring_active = False
        
    async def initialize(self):
        """Initialize connections and setup MCP server"""
        try:
            self.redis_client = redis.from_url(settings.redis_url)
            await self._setup_mcp_resources()
            await self._setup_mcp_tools()
            logger.info("Pylon customer intelligence initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Pylon customer intelligence: {e}")
            raise
        
    async def _setup_mcp_resources(self):
        """Setup MCP resources for customer data"""
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            return [
                Resource(
                    uri="pylon://customers/churn-risk",
                    name="Customer Churn Risk Analysis",
                    mimeType="application/json",
                    description="Real-time customer churn risk assessment and predictions"
                ),
                Resource(
                    uri="pylon://support/satisfaction",
                    name="Support Satisfaction Metrics",
                    mimeType="application/json",
                    description="Customer support satisfaction scores and trends"
                ),
                Resource(
                    uri="pylon://customers/health-score",
                    name="Customer Health Score",
                    mimeType="application/json", 
                    description="Comprehensive customer health and engagement metrics"
                ),
                Resource(
                    uri="pylon://tickets/critical",
                    name="Critical Support Tickets",
                    mimeType="application/json",
                    description="Critical and escalated support tickets requiring attention"
                )
            ]
            
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            try:
                if uri == "pylon://customers/churn-risk":
                    data = await self._analyze_churn_risk()
                elif uri == "pylon://support/satisfaction":
                    data = await self._get_satisfaction_metrics()
                elif uri == "pylon://customers/health-score":
                    data = await self._calculate_customer_health()
                elif uri == "pylon://tickets/critical":
                    data = await self._get_critical_tickets()
                else:
                    raise ValueError(f"Unknown resource: {uri}")
                return json.dumps(data, indent=2)
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                return json.dumps({"error": str(e)}, indent=2)
    
    async def _setup_mcp_tools(self):
        """Setup MCP tools for customer actions"""
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="escalate_customer_issue",
                    description="Automatically escalate critical customer issues to appropriate teams",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "issue_type": {"type": "string", "enum": ["churn_risk", "technical", "billing", "satisfaction"]},
                            "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                            "reason": {"type": "string"}
                        },
                        "required": ["customer_id", "issue_type", "priority", "reason"]
                    }
                ),
                Tool(
                    name="launch_retention_campaign",
                    description="Launch targeted customer retention campaign for at-risk customers",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "customer_segment": {"type": "string"},
                            "campaign_type": {"type": "string", "enum": ["discount", "feature_highlight", "success_check", "upgrade_offer"]},
                            "urgency": {"type": "string", "enum": ["low", "medium", "high"]},
                            "personalization_data": {"type": "object"}
                        },
                        "required": ["customer_segment", "campaign_type"]
                    }
                ),
                Tool(
                    name="schedule_health_check",
                    description="Schedule proactive customer success health check",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "customer_ids": {"type": "array", "items": {"type": "string"}},
                            "check_type": {"type": "string", "enum": ["usage_review", "satisfaction_survey", "feature_adoption", "expansion_opportunity"]},
                            "timeline": {"type": "string", "enum": ["immediate", "within_24h", "within_week"]}
                        },
                        "required": ["customer_ids", "check_type", "timeline"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            try:
                if name == "escalate_customer_issue":
                    result = await self._escalate_customer_issue(arguments)
                elif name == "launch_retention_campaign":
                    result = await self._launch_retention_campaign(arguments)
                elif name == "schedule_health_check":
                    result = await self._schedule_health_check(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]
    
    async def start_monitoring(self):
        """Start continuous customer intelligence monitoring"""
        self.monitoring_active = True
        logger.info("Starting Pylon customer monitoring")
        
        tasks = [
            asyncio.create_task(self._monitor_churn_risk()),
            asyncio.create_task(self._monitor_satisfaction_scores()),
            asyncio.create_task(self._monitor_critical_tickets()),
            asyncio.create_task(self._monitor_customer_health())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error in customer monitoring: {e}")
    
    async def _monitor_churn_risk(self):
        """Monitor customer churn risk continuously"""
        while self.monitoring_active:
            try:
                churn_data = await self._analyze_churn_risk()
                
                high_risk_customers = [
                    customer for customer in churn_data.get('customers', [])
                    if customer.get('churn_risk_score', 0) > settings.high_churn_risk_threshold
                ]
                
                if high_risk_customers:
                    await self._publish_customer_alert({
                        'alert_type': 'high_churn_risk',
                        'customer_count': len(high_risk_customers),
                        'customers': high_risk_customers,
                        'severity': 'high',
                        'data': churn_data
                    })
                
                # Check for churn risk trends
                risk_trend = churn_data.get('trend_analysis', {})
                if risk_trend.get('increasing_risk_customers', 0) > 5:
                    await self._publish_customer_alert({
                        'alert_type': 'churn_risk_trend',
                        'trend_data': risk_trend,
                        'severity': 'medium',
                        'data': churn_data
                    })
                
                await asyncio.sleep(1800)  # Check every 30 minutes
                
            except Exception as e:
                logger.error(f"Error monitoring churn risk: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_satisfaction_scores(self):
        """Monitor customer satisfaction scores"""
        while self.monitoring_active:
            try:
                satisfaction_data = await self._get_satisfaction_metrics()
                
                # Check for declining satisfaction
                avg_score = satisfaction_data.get('average_score', 5.0)
                if avg_score < 3.5:  # Below 3.5/5 threshold
                    await self._publish_customer_alert({
                        'alert_type': 'low_satisfaction',
                        'average_score': avg_score,
                        'severity': 'high',
                        'data': satisfaction_data
                    })
                
                # Check for negative trend
                trend = satisfaction_data.get('trend_analysis', {})
                if trend.get('direction') == 'declining' and trend.get('change_percent', 0) < -10:
                    await self._publish_customer_alert({
                        'alert_type': 'satisfaction_decline',
                        'trend_data': trend,
                        'severity': 'medium',
                        'data': satisfaction_data
                    })
                
                await asyncio.sleep(3600)  # Check every hour
                
            except Exception as e:
                logger.error(f"Error monitoring satisfaction: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_critical_tickets(self):
        """Monitor critical support tickets"""
        while self.monitoring_active:
            try:
                critical_tickets = await self._get_critical_tickets()
                
                # Check for unresolved critical tickets
                unresolved = [
                    ticket for ticket in critical_tickets.get('tickets', [])
                    if ticket.get('status') not in ['resolved', 'closed']
                ]
                
                if unresolved:
                    # Check for tickets open too long
                    overdue_tickets = []
                    for ticket in unresolved:
                        created_at = datetime.fromisoformat(ticket.get('created_at', '').replace('Z', '+00:00'))
                        hours_open = (datetime.now() - created_at).total_seconds() / 3600
                        
                        if hours_open > 4:  # Critical tickets open > 4 hours
                            overdue_tickets.append({**ticket, 'hours_open': hours_open})
                    
                    if overdue_tickets:
                        await self._publish_customer_alert({
                            'alert_type': 'overdue_critical_tickets',
                            'ticket_count': len(overdue_tickets),
                            'tickets': overdue_tickets,
                            'severity': 'critical',
                            'data': critical_tickets
                        })
                
                await asyncio.sleep(600)  # Check every 10 minutes
                
            except Exception as e:
                logger.error(f"Error monitoring critical tickets: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_customer_health(self):
        """Monitor overall customer health trends"""
        while self.monitoring_active:
            try:
                health_data = await self._calculate_customer_health()
                
                # Check for customers with declining health
                declining_customers = [
                    customer for customer in health_data.get('customers', [])
                    if customer.get('health_trend') == 'declining' 
                    and customer.get('health_score', 100) < 60
                ]
                
                if declining_customers:
                    await self._publish_customer_alert({
                        'alert_type': 'declining_customer_health',
                        'customer_count': len(declining_customers),
                        'customers': declining_customers[:10],  # Top 10 most at-risk
                        'severity': 'medium',
                        'data': health_data
                    })
                
                await asyncio.sleep(7200)  # Check every 2 hours
                
            except Exception as e:
                logger.error(f"Error monitoring customer health: {e}")
                await asyncio.sleep(300)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _analyze_churn_risk(self) -> Dict[str, Any]:
        """Analyze customer churn risk using Pylon API"""
        try:
            # Get customer data
            response = await self.http_client.get("/api/v1/customers")
            response.raise_for_status()
            customers = response.json().get('data', [])
            
            # Get usage analytics
            usage_response = await self.http_client.get("/api/v1/analytics/usage")
            usage_response.raise_for_status()
            usage_data = usage_response.json().get('data', {})
            
            # Calculate churn risk scores
            customer_risk_analysis = []
            total_high_risk = 0
            
            for customer in customers:
                customer_id = customer.get('id')
                
                # Calculate risk factors
                risk_factors = await self._calculate_risk_factors(customer, usage_data)
                churn_risk_score = self._calculate_churn_score(risk_factors)
                
                if churn_risk_score > settings.high_churn_risk_threshold:
                    total_high_risk += 1
                
                customer_analysis = {
                    'customer_id': customer_id,
                    'customer_name': customer.get('name', ''),
                    'churn_risk_score': churn_risk_score,
                    'risk_factors': risk_factors,
                    'risk_level': self._get_risk_level(churn_risk_score),
                    'last_activity': customer.get('last_activity_date'),
                    'account_value': customer.get('monthly_value', 0)
                }
                
                customer_risk_analysis.append(customer_analysis)
            
            # Sort by risk score
            customer_risk_analysis.sort(key=lambda x: x['churn_risk_score'], reverse=True)
            
            # Analyze trends
            trend_analysis = await self._analyze_churn_trends(customer_risk_analysis)
            
            return {
                'total_customers': len(customers),
                'high_risk_customers': total_high_risk,
                'customers': customer_risk_analysis[:50],  # Top 50 at-risk
                'trend_analysis': trend_analysis,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing churn risk: {e}")
            return {'error': str(e)}
    
    async def _calculate_risk_factors(self, customer: Dict, usage_data: Dict) -> Dict[str, float]:
        """Calculate individual risk factors for a customer"""
        customer_id = customer.get('id')
        
        # Usage-based factors
        recent_usage = usage_data.get(customer_id, {}).get('last_30_days', 0)
        previous_usage = usage_data.get(customer_id, {}).get('previous_30_days', 1)
        usage_trend = (recent_usage - previous_usage) / previous_usage if previous_usage > 0 else 0
        
        # Engagement factors
        last_login = customer.get('last_login_date')
        days_since_login = 0
        if last_login:
            last_login_date = datetime.fromisoformat(last_login.replace('Z', '+00:00'))
            days_since_login = (datetime.now() - last_login_date).days
        
        # Support factors
        open_tickets = customer.get('open_support_tickets', 0)
        satisfaction_score = customer.get('last_satisfaction_score', 5.0)
        
        # Financial factors
        payment_issues = customer.get('payment_failures', 0)
        subscription_changes = customer.get('recent_downgrades', 0)
        
        return {
            'usage_decline': max(0, -usage_trend),  # Negative trend = higher risk
            'login_recency': min(days_since_login / 30, 1.0),  # Normalize to 0-1
            'support_burden': min(open_tickets / 10, 1.0),  # Normalize to 0-1
            'satisfaction': (5.0 - satisfaction_score) / 4.0,  # Invert and normalize
            'payment_risk': min(payment_issues / 3, 1.0),  # Normalize to 0-1
            'subscription_risk': min(subscription_changes / 2, 1.0)  # Normalize to 0-1
        }
    
    def _calculate_churn_score(self, risk_factors: Dict[str, float]) -> float:
        """Calculate overall churn risk score from individual factors"""
        weights = {
            'usage_decline': 0.25,
            'login_recency': 0.20,
            'support_burden': 0.15,
            'satisfaction': 0.20,
            'payment_risk': 0.15,
            'subscription_risk': 0.05
        }
        
        weighted_score = sum(
            risk_factors.get(factor, 0) * weight 
            for factor, weight in weights.items()
        )
        
        return min(weighted_score, 1.0)  # Cap at 1.0
    
    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to risk level"""
        if score >= 0.8:
            return 'critical'
        elif score >= 0.6:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    async def _analyze_churn_trends(self, customer_analysis: List[Dict]) -> Dict[str, Any]:
        """Analyze trends in churn risk"""
        try:
            # Get historical churn data for comparison
            current_high_risk = len([c for c in customer_analysis if c['churn_risk_score'] > 0.6])
            current_critical_risk = len([c for c in customer_analysis if c['churn_risk_score'] > 0.8])
            
            # Calculate trend metrics (simplified)
            return {
                'current_high_risk': current_high_risk,
                'current_critical_risk': current_critical_risk,
                'increasing_risk_customers': current_high_risk,  # Placeholder - would compare to historical
                'trend_direction': 'stable',  # Placeholder - would calculate from historical data
                'risk_distribution': {
                    'critical': current_critical_risk,
                    'high': current_high_risk - current_critical_risk,
                    'medium': len([c for c in customer_analysis if 0.4 <= c['churn_risk_score'] < 0.6]),
                    'low': len([c for c in customer_analysis if c['churn_risk_score'] < 0.4])
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing churn trends: {e}")
            return {}
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _get_satisfaction_metrics(self) -> Dict[str, Any]:
        """Get customer satisfaction metrics"""
        try:
            response = await self.http_client.get("/api/v1/satisfaction/metrics")
            response.raise_for_status()
            data = response.json().get('data', {})
            
            return {
                'average_score': data.get('average_rating', 0),
                'total_responses': data.get('total_surveys', 0),
                'response_rate': data.get('response_rate', 0),
                'score_distribution': data.get('score_breakdown', {}),
                'trend_analysis': {
                    'direction': data.get('trend_direction', 'stable'),
                    'change_percent': data.get('trend_change_percent', 0)
                },
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting satisfaction metrics: {e}")
            return {'error': str(e)}
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _calculate_customer_health(self) -> Dict[str, Any]:
        """Calculate comprehensive customer health scores"""
        try:
            response = await self.http_client.get("/api/v1/customers/health")
            response.raise_for_status()
            data = response.json().get('data', [])
            
            customer_health = []
            for customer in data:
                health_score = self._calculate_health_score(customer)
                
                customer_health.append({
                    'customer_id': customer.get('id'),
                    'customer_name': customer.get('name', ''),
                    'health_score': health_score,
                    'health_trend': customer.get('trend', 'stable'),
                    'key_metrics': {
                        'usage_score': customer.get('usage_score', 0),
                        'engagement_score': customer.get('engagement_score', 0),
                        'satisfaction_score': customer.get('satisfaction_score', 0),
                        'financial_score': customer.get('financial_health', 0)
                    },
                    'last_assessment': datetime.now().isoformat()
                })
            
            return {
                'customers': customer_health,
                'overall_health': sum(c['health_score'] for c in customer_health) / len(customer_health) if customer_health else 0,
                'assessment_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calculating customer health: {e}")
            return {'error': str(e)}
    
    def _calculate_health_score(self, customer: Dict) -> float:
        """Calculate overall customer health score"""
        usage_score = customer.get('usage_score', 0)
        engagement_score = customer.get('engagement_score', 0) 
        satisfaction_score = customer.get('satisfaction_score', 0)
        financial_score = customer.get('financial_health', 0)
        
        # Weighted average
        weights = [0.3, 0.3, 0.25, 0.15]  # Usage, Engagement, Satisfaction, Financial
        scores = [usage_score, engagement_score, satisfaction_score, financial_score]
        
        health_score = sum(score * weight for score, weight in zip(scores, weights))
        return min(max(health_score, 0), 100)  # Clamp between 0-100
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _get_critical_tickets(self) -> Dict[str, Any]:
        """Get critical and escalated support tickets"""
        try:
            response = await self.http_client.get("/api/v1/tickets/critical")
            response.raise_for_status()
            tickets = response.json().get('data', [])
            
            return {
                'tickets': tickets,
                'total_critical': len(tickets),
                'unresolved_count': len([t for t in tickets if t.get('status') not in ['resolved', 'closed']]),
                'average_resolution_time': self._calculate_avg_resolution_time(tickets),
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting critical tickets: {e}")
            return {'error': str(e)}
    
    def _calculate_avg_resolution_time(self, tickets: List[Dict]) -> float:
        """Calculate average resolution time for tickets"""
        resolved_tickets = [t for t in tickets if t.get('status') in ['resolved', 'closed']]
        
        if not resolved_tickets:
            return 0.0
        
        total_time = 0
        for ticket in resolved_tickets:
            created_at = datetime.fromisoformat(ticket.get('created_at', '').replace('Z', '+00:00'))
            resolved_at = datetime.fromisoformat(ticket.get('resolved_at', '').replace('Z', '+00:00'))
            resolution_time = (resolved_at - created_at).total_seconds() / 3600  # Hours
            total_time += resolution_time
        
        return total_time / len(resolved_tickets)
    
    async def _escalate_customer_issue(self, args: Dict) -> Dict[str, Any]:
        """Escalate customer issue to appropriate teams"""
        try:
            customer_id = args['customer_id']
            issue_type = args['issue_type']
            priority = args['priority']
            reason = args['reason']
            
            # Create escalation record
            escalation_data = {
                'customer_id': customer_id,
                'issue_type': issue_type,
                'priority': priority,
                'reason': reason,
                'escalated_at': datetime.now().isoformat(),
                'escalated_by': 'pensieve_cio'
            }
            
            # Send to appropriate team based on issue type
            team_assignments = {
                'churn_risk': 'customer_success',
                'technical': 'engineering_support',
                'billing': 'finance_team',
                'satisfaction': 'customer_success'
            }
            
            assigned_team = team_assignments.get(issue_type, 'customer_success')
            
            # Post escalation via Pylon API
            response = await self.http_client.post(
                "/api/v1/escalations",
                json={
                    **escalation_data,
                    'assigned_team': assigned_team
                }
            )
            response.raise_for_status()
            
            return {
                'escalation_id': response.json().get('id'),
                'customer_id': customer_id,
                'assigned_team': assigned_team,
                'priority': priority,
                'status': 'escalated',
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error escalating customer issue: {e}")
            return {'error': str(e)}
    
    async def _launch_retention_campaign(self, args: Dict) -> Dict[str, Any]:
        """Launch targeted retention campaign"""
        try:
            customer_segment = args['customer_segment']
            campaign_type = args['campaign_type']
            urgency = args.get('urgency', 'medium')
            personalization = args.get('personalization_data', {})
            
            campaign_data = {
                'campaign_type': campaign_type,
                'target_segment': customer_segment,
                'urgency_level': urgency,
                'personalization': personalization,
                'launched_at': datetime.now().isoformat(),
                'launched_by': 'pensieve_cio'
            }
            
            # Launch campaign via Pylon API
            response = await self.http_client.post(
                "/api/v1/campaigns/retention",
                json=campaign_data
            )
            response.raise_for_status()
            
            return {
                'campaign_id': response.json().get('id'),
                'campaign_type': campaign_type,
                'target_segment': customer_segment,
                'estimated_reach': response.json().get('estimated_reach', 0),
                'status': 'launched',
                'launched_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error launching retention campaign: {e}")
            return {'error': str(e)}
    
    async def _schedule_health_check(self, args: Dict) -> Dict[str, Any]:
        """Schedule customer health check"""
        try:
            customer_ids = args['customer_ids']
            check_type = args['check_type']
            timeline = args['timeline']
            
            # Calculate scheduled date based on timeline
            schedule_mapping = {
                'immediate': datetime.now(),
                'within_24h': datetime.now() + timedelta(hours=8),
                'within_week': datetime.now() + timedelta(days=2)
            }
            
            scheduled_date = schedule_mapping.get(timeline, datetime.now() + timedelta(hours=24))
            
            health_check_data = {
                'customer_ids': customer_ids,
                'check_type': check_type,
                'scheduled_date': scheduled_date.isoformat(),
                'created_by': 'pensieve_cio'
            }
            
            # Schedule via Pylon API
            response = await self.http_client.post(
                "/api/v1/health-checks/schedule",
                json=health_check_data
            )
            response.raise_for_status()
            
            return {
                'health_check_id': response.json().get('id'),
                'customer_count': len(customer_ids),
                'check_type': check_type,
                'scheduled_date': scheduled_date.isoformat(),
                'status': 'scheduled'
            }
            
        except Exception as e:
            logger.error(f"Error scheduling health check: {e}")
            return {'error': str(e)}
    
    async def _publish_customer_alert(self, alert_data: Dict):
        """Publish customer alert to Redis stream"""
        try:
            await self.redis_client.xadd(
                'pylon_events',
                {
                    'data': json.dumps(alert_data),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'pylon_customer_intelligence'
                }
            )
            logger.info(f"Published customer alert: {alert_data['alert_type']}")
        except Exception as e:
            logger.error(f"Error publishing customer alert: {e}")