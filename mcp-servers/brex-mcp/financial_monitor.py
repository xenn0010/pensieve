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
from mock_financial_data import MockFinancialDataGenerator, DEMO_PROFILES, FinancialScenario

logger = logging.getLogger(__name__)


class BrexFinancialMonitor:
    def __init__(self):
        self.server = Server("brex-financial-monitor")
        # Use mock data instead of real API
        self.use_mock_data = True
        self.mock_generator = None
        
        # Keep HTTP client for potential future real API use
        self.http_client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {settings.brex_api_key}"},
            timeout=30.0
        ) if settings.brex_api_key else None
        
        self.redis_client = None
        self.monitoring_active = False
        
    async def initialize(self):
        """Initialize connections and setup MCP server"""
        try:
            self.redis_client = redis.from_url(settings.redis_url)
            
            # Initialize mock data generator
            if self.use_mock_data:
                # Use a predefined profile or generate random one
                demo_profile = getattr(settings, 'demo_financial_profile', 'healthy_saas')
                if demo_profile in DEMO_PROFILES:
                    self.mock_generator = MockFinancialDataGenerator(DEMO_PROFILES[demo_profile])
                    logger.info(f"Initialized mock financial data with profile: {demo_profile}")
                else:
                    self.mock_generator = MockFinancialDataGenerator()
                    logger.info("Initialized mock financial data with random profile")
            
            await self._setup_mcp_resources()
            await self._setup_mcp_tools()
            logger.info("Brex financial monitor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Brex financial monitor: {e}")
            raise
        
    async def _setup_mcp_resources(self):
        """Setup MCP resources for financial data"""
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            return [
                Resource(
                    uri="brex://cash-flow/current",
                    name="Current Cash Flow",
                    mimeType="application/json",
                    description="Real-time cash flow and runway analysis"
                ),
                Resource(
                    uri="brex://expenses/analysis",
                    name="Expense Analysis", 
                    mimeType="application/json",
                    description="Categorized expense analysis and trends"
                ),
                Resource(
                    uri="brex://burn-rate/prediction",
                    name="Burn Rate Prediction",
                    mimeType="application/json", 
                    description="Predictive burn rate analysis"
                )
            ]
            
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            if uri == "brex://cash-flow/current":
                data = await self._get_current_cash_flow()
                return json.dumps(data, indent=2)
            elif uri == "brex://expenses/analysis":
                data = await self._analyze_expenses()
                return json.dumps(data, indent=2)
            elif uri == "brex://burn-rate/prediction":
                data = await self._predict_burn_rate()
                return json.dumps(data, indent=2)
            else:
                raise ValueError(f"Unknown resource: {uri}")
    
    async def _setup_mcp_tools(self):
        """Setup MCP tools for financial actions"""
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="optimize_cash_flow",
                    description="Automatically optimize cash flow based on current financial state",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "strategy": {"type": "string", "enum": ["conservative", "aggressive", "balanced"]},
                            "target_runway_days": {"type": "integer", "minimum": 30}
                        },
                        "required": ["strategy"]
                    }
                ),
                Tool(
                    name="emergency_funding_prep",
                    description="Prepare emergency funding documentation and projections",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "funding_amount": {"type": "integer", "minimum": 100000},
                            "urgency_level": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
                        },
                        "required": ["urgency_level"]
                    }
                ),
                Tool(
                    name="expense_optimization",
                    description="Identify and implement expense optimization opportunities", 
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "categories": {"type": "array", "items": {"type": "string"}},
                            "target_reduction_percent": {"type": "number", "minimum": 0, "maximum": 50}
                        }
                    }
                ),
                Tool(
                    name="simulate_financial_scenario",
                    description="Simulate different financial scenarios for testing AI responses",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scenario": {"type": "string", "enum": ["critical_runway", "burn_rate_spike", "revenue_drop", "large_expense", "healthy_growth"]},
                            "profile": {"type": "string", "enum": ["healthy_saas", "cash_crunch_startup", "post_funding_scale", "seasonal_ecommerce"], "description": "Optional: change company profile"}
                        },
                        "required": ["scenario"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            try:
                if name == "optimize_cash_flow":
                    result = await self._optimize_cash_flow(arguments)
                elif name == "emergency_funding_prep":
                    result = await self._prepare_emergency_funding(arguments)
                elif name == "expense_optimization":
                    result = await self._optimize_expenses(arguments)
                elif name == "simulate_financial_scenario":
                    result = await self._simulate_financial_scenario(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]
    
    async def start_monitoring(self):
        """Start continuous financial monitoring"""
        self.monitoring_active = True
        
        tasks = [
            asyncio.create_task(self._monitor_cash_flow()),
            asyncio.create_task(self._monitor_burn_rate()),
            asyncio.create_task(self._monitor_large_expenses()),
            asyncio.create_task(self._monitor_payment_delays())
        ]
        
        await asyncio.gather(*tasks)
    
    async def _monitor_cash_flow(self):
        """Monitor cash flow for critical changes"""
        while self.monitoring_active:
            try:
                cash_flow_data = await self._get_current_cash_flow()
                
                # Check for critical cash flow situations
                runway_days = cash_flow_data.get('runway_days', float('inf'))
                if runway_days < settings.critical_cash_runway_days:
                    await self._publish_financial_alert({
                        'alert_type': 'critical_runway',
                        'runway_days': runway_days,
                        'severity': 'critical',
                        'data': cash_flow_data
                    })
                
                # Check for unusual cash flow patterns
                burn_rate_change = cash_flow_data.get('burn_rate_change_percent', 0)
                if abs(burn_rate_change) > 25:  # 25% change in burn rate
                    await self._publish_financial_alert({
                        'alert_type': 'burn_rate_anomaly', 
                        'change_percent': burn_rate_change,
                        'severity': 'high',
                        'data': cash_flow_data
                    })
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                print(f"Error monitoring cash flow: {e}")
                await asyncio.sleep(60)
    
    async def _monitor_burn_rate(self):
        """Monitor burn rate trends and predictions"""
        while self.monitoring_active:
            try:
                burn_data = await self._predict_burn_rate()
                
                # Check for accelerating burn rate
                predicted_increase = burn_data.get('predicted_increase_percent', 0)
                if predicted_increase > 20:
                    await self._publish_financial_alert({
                        'alert_type': 'accelerating_burn',
                        'predicted_increase': predicted_increase,
                        'severity': 'high', 
                        'data': burn_data
                    })
                
                await asyncio.sleep(3600)  # Check every hour
                
            except Exception as e:
                print(f"Error monitoring burn rate: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_large_expenses(self):
        """Monitor for unusually large expenses"""
        while self.monitoring_active:
            try:
                recent_expenses = await self._get_recent_large_expenses()
                
                for expense in recent_expenses:
                    if expense.get('amount', 0) > 10000:  # $10k threshold
                        await self._publish_financial_alert({
                            'alert_type': 'large_expense',
                            'expense': expense,
                            'severity': 'medium',
                            'data': {'expense_details': expense}
                        })
                
                await asyncio.sleep(1800)  # Check every 30 minutes
                
            except Exception as e:
                print(f"Error monitoring large expenses: {e}")
                await asyncio.sleep(300)
    
    async def _monitor_payment_delays(self):
        """Monitor for payment processing delays"""
        while self.monitoring_active:
            try:
                payment_status = await self._check_payment_status()
                
                delayed_payments = payment_status.get('delayed_payments', [])
                if delayed_payments:
                    await self._publish_financial_alert({
                        'alert_type': 'payment_delays',
                        'delayed_count': len(delayed_payments),
                        'severity': 'medium',
                        'data': {'delayed_payments': delayed_payments}
                    })
                
                await asyncio.sleep(900)  # Check every 15 minutes
                
            except Exception as e:
                print(f"Error monitoring payments: {e}")
                await asyncio.sleep(300)
    
    async def _get_current_cash_flow(self) -> Dict[str, Any]:
        """Get current cash flow data from mock generator or Brex API"""
        try:
            if self.use_mock_data and self.mock_generator:
                return self.mock_generator.get_current_cash_flow_data()
            
            # Original Brex API code (kept for future use)
            if self.http_client:
                response = await self.http_client.get("/v2/accounts")
                accounts = response.json()
                
                total_balance = sum(account.get('balance', {}).get('amount', 0) for account in accounts.get('data', []))
                
                # Calculate burn rate (simplified)
                burn_rate = await self._calculate_burn_rate()
                runway_days = int(total_balance / burn_rate) if burn_rate > 0 else float('inf')
                
                return {
                    'total_balance': total_balance,
                    'burn_rate_monthly': burn_rate,
                    'runway_days': runway_days,
                    'accounts': len(accounts.get('data', [])),
                    'last_updated': datetime.now().isoformat(),
                    'burn_rate_change_percent': await self._calculate_burn_rate_change()
                }
            else:
                return {'error': 'No API client or mock generator available'}
            
        except Exception as e:
            logger.error(f"Error getting cash flow data: {e}")
            return {'error': str(e)}
    
    async def _calculate_burn_rate(self) -> float:
        """Calculate monthly burn rate"""
        try:
            if self.use_mock_data and self.mock_generator:
                # Get cash flow data which includes calculated burn rate
                cash_flow_data = self.mock_generator.get_current_cash_flow_data()
                return cash_flow_data.get('burn_rate_monthly', 0)
            
            # Original Brex API code
            if self.http_client:
                # Get transactions from last 90 days
                end_date = datetime.now()
                start_date = end_date - timedelta(days=90)
                
                response = await self.http_client.get(
                    "/v2/transactions",
                    params={
                        'posted_at_start': start_date.isoformat(),
                        'posted_at_end': end_date.isoformat()
                    }
                )
                
                transactions = response.json().get('data', [])
                
                # Calculate total outflows
                total_outflow = sum(
                    abs(tx.get('amount', {}).get('amount', 0))
                    for tx in transactions
                    if tx.get('amount', {}).get('amount', 0) < 0
                )
                
                # Convert to monthly burn rate
                monthly_burn = (total_outflow / 90) * 30
                return monthly_burn
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating burn rate: {e}")
            return 0.0
    
    async def _calculate_burn_rate_change(self) -> float:
        """Calculate burn rate change percentage"""
        try:
            if self.use_mock_data and self.mock_generator:
                # Mock generator already calculates this
                cash_flow_data = self.mock_generator.get_current_cash_flow_data()
                return cash_flow_data.get('burn_rate_change_percent', 0)
            
            # Original Brex API code
            if self.http_client:
                # Get current month vs previous month burn rates
                current_burn = await self._get_period_burn_rate(30)
                previous_burn = await self._get_period_burn_rate(30, offset_days=30)
                
                if previous_burn > 0:
                    change_percent = ((current_burn - previous_burn) / previous_burn) * 100
                    return change_percent
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating burn rate change: {e}")
            return 0.0
    
    async def _get_period_burn_rate(self, days: int, offset_days: int = 0) -> float:
        """Get burn rate for a specific period"""
        try:
            end_date = datetime.now() - timedelta(days=offset_days)
            start_date = end_date - timedelta(days=days)
            
            response = await self.http_client.get(
                "/v2/transactions",
                params={
                    'posted_at_start': start_date.isoformat(),
                    'posted_at_end': end_date.isoformat()
                }
            )
            
            transactions = response.json().get('data', [])
            total_outflow = sum(
                abs(tx.get('amount', {}).get('amount', 0))
                for tx in transactions
                if tx.get('amount', {}).get('amount', 0) < 0
            )
            
            return total_outflow
            
        except Exception as e:
            print(f"Error getting period burn rate: {e}")
            return 0.0
    
    async def _analyze_expenses(self) -> Dict[str, Any]:
        """Analyze expense patterns and categories"""
        try:
            if self.use_mock_data and self.mock_generator:
                return self.mock_generator.get_expense_analysis()
            
            # Original Brex API code
            if self.http_client:
                # Get recent transactions
                response = await self.http_client.get(
                    "/v2/transactions",
                    params={'limit': 1000}
                )
                
                transactions = response.json().get('data', [])
                
                # Categorize expenses
                categories = {}
                for tx in transactions:
                    if tx.get('amount', {}).get('amount', 0) < 0:  # Outgoing
                        category = tx.get('merchant', {}).get('mcc_description', 'Other')
                        amount = abs(tx.get('amount', {}).get('amount', 0))
                        
                        if category not in categories:
                            categories[category] = {'total': 0, 'count': 0, 'transactions': []}
                        
                        categories[category]['total'] += amount
                        categories[category]['count'] += 1
                        categories[category]['transactions'].append(tx)
                
                # Sort by total spend
                sorted_categories = sorted(
                    categories.items(),
                    key=lambda x: x[1]['total'],
                    reverse=True
                )
                
                return {
                    'categories': dict(sorted_categories[:10]),  # Top 10 categories
                    'total_transactions': len(transactions),
                    'analysis_date': datetime.now().isoformat()
                }
            
            return {'error': 'No API client or mock generator available'}
            
        except Exception as e:
            logger.error(f"Error analyzing expenses: {e}")
            return {'error': str(e)}
    
    async def _predict_burn_rate(self) -> Dict[str, Any]:
        """Predict future burn rate trends"""
        try:
            # Get historical burn rates
            current_burn = await self._get_period_burn_rate(30)
            previous_burn = await self._get_period_burn_rate(30, offset_days=30)
            historical_burn = await self._get_period_burn_rate(30, offset_days=60)
            
            # Simple trend analysis
            if previous_burn > 0:
                trend = (current_burn - previous_burn) / previous_burn
            else:
                trend = 0
            
            # Predict next month
            predicted_burn = current_burn * (1 + trend)
            predicted_increase = ((predicted_burn - current_burn) / current_burn * 100) if current_burn > 0 else 0
            
            return {
                'current_monthly_burn': current_burn,
                'predicted_monthly_burn': predicted_burn, 
                'predicted_increase_percent': predicted_increase,
                'trend_direction': 'increasing' if trend > 0 else 'decreasing',
                'confidence': min(abs(trend) * 100, 95),  # Confidence based on trend strength
                'prediction_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error predicting burn rate: {e}")
            return {'error': str(e)}
    
    async def _get_recent_large_expenses(self) -> List[Dict]:
        """Get recent large expenses for monitoring"""
        try:
            if self.use_mock_data and self.mock_generator:
                return self.mock_generator.get_large_recent_expenses()
            
            # Original Brex API code
            if self.http_client:
                response = await self.http_client.get(
                    "/v2/transactions",
                    params={
                        'limit': 100,
                        'posted_at_start': (datetime.now() - timedelta(days=1)).isoformat()
                    }
                )
                
                transactions = response.json().get('data', [])
                
                # Filter for large outgoing transactions
                large_expenses = [
                    tx for tx in transactions
                    if tx.get('amount', {}).get('amount', 0) < -5000  # More than $5k outgoing
                ]
                
                return large_expenses
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting large expenses: {e}")
            return []
    
    async def _check_payment_status(self) -> Dict[str, Any]:
        """Check for delayed or failed payments"""
        try:
            # Get recent transfers/payments
            response = await self.http_client.get("/v2/transfers")
            transfers = response.json().get('data', [])
            
            delayed_payments = [
                transfer for transfer in transfers
                if transfer.get('status') in ['pending', 'processing']
                and (datetime.now() - datetime.fromisoformat(
                    transfer.get('created_at', '').replace('Z', '+00:00')
                )).days > 2
            ]
            
            return {
                'total_transfers': len(transfers),
                'delayed_payments': delayed_payments,
                'check_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error checking payment status: {e}")
            return {'error': str(e)}
    
    async def _optimize_cash_flow(self, args: Dict) -> Dict[str, Any]:
        """Optimize cash flow based on strategy"""
        strategy = args.get('strategy', 'balanced')
        target_runway = args.get('target_runway_days', 90)
        
        current_data = await self._get_current_cash_flow()
        current_runway = current_data.get('runway_days', 0)
        
        if current_runway < target_runway:
            # Need to extend runway
            required_reduction = 1 - (current_runway / target_runway)
            
            recommendations = []
            if strategy == 'aggressive':
                recommendations.append({
                    'action': 'immediate_expense_freeze',
                    'description': 'Freeze all non-essential expenses immediately',
                    'impact': f'Could extend runway by {int(required_reduction * 30)} days'
                })
            elif strategy == 'balanced':
                recommendations.append({
                    'action': 'strategic_expense_review',
                    'description': 'Review and reduce discretionary spending',
                    'impact': f'Could extend runway by {int(required_reduction * 20)} days'
                })
            else:  # conservative
                recommendations.append({
                    'action': 'gradual_optimization',
                    'description': 'Gradually optimize expenses over 30 days',
                    'impact': f'Could extend runway by {int(required_reduction * 15)} days'
                })
            
            return {
                'current_runway_days': current_runway,
                'target_runway_days': target_runway,
                'required_reduction_percent': required_reduction * 100,
                'recommendations': recommendations,
                'strategy_applied': strategy
            }
        
        return {
            'current_runway_days': current_runway,
            'target_runway_days': target_runway,
            'status': 'runway_adequate',
            'strategy_applied': strategy
        }
    
    async def _prepare_emergency_funding(self, args: Dict) -> Dict[str, Any]:
        """Prepare emergency funding materials"""
        urgency = args.get('urgency_level', 'medium')
        funding_amount = args.get('funding_amount', 1000000)
        
        current_data = await self._get_current_cash_flow()
        burn_data = await self._predict_burn_rate()
        
        # Generate funding justification
        justification = {
            'current_runway_days': current_data.get('runway_days', 0),
            'monthly_burn_rate': burn_data.get('current_monthly_burn', 0),
            'funding_amount_requested': funding_amount,
            'extended_runway_days': int(funding_amount / (burn_data.get('current_monthly_burn', 1) / 30)),
            'urgency_level': urgency
        }
        
        # Create funding deck outline
        deck_outline = [
            'Current Financial Position',
            'Burn Rate Analysis & Projections', 
            'Funding Requirements & Use of Funds',
            'Extended Runway Calculations',
            'Risk Mitigation Strategies'
        ]
        
        return {
            'funding_justification': justification,
            'deck_outline': deck_outline,
            'recommended_timeline': '2-4 weeks' if urgency == 'critical' else '4-8 weeks',
            'preparation_status': 'draft_ready',
            'generated_at': datetime.now().isoformat()
        }
    
    async def _optimize_expenses(self, args: Dict) -> Dict[str, Any]:
        """Identify expense optimization opportunities"""
        categories = args.get('categories', [])
        target_reduction = args.get('target_reduction_percent', 15)
        
        expense_data = await self._analyze_expenses()
        
        optimization_opportunities = []
        total_potential_savings = 0
        
        for category, data in expense_data.get('categories', {}).items():
            if not categories or category in categories:
                category_savings = data['total'] * (target_reduction / 100)
                total_potential_savings += category_savings
                
                optimization_opportunities.append({
                    'category': category,
                    'current_spend': data['total'],
                    'potential_savings': category_savings,
                    'transaction_count': data['count'],
                    'optimization_suggestions': self._get_category_suggestions(category)
                })
        
        return {
            'optimization_opportunities': optimization_opportunities,
            'total_potential_monthly_savings': total_potential_savings,
            'target_reduction_percent': target_reduction,
            'affected_categories': len(optimization_opportunities),
            'generated_at': datetime.now().isoformat()
        }
    
    def _get_category_suggestions(self, category: str) -> List[str]:
        """Get optimization suggestions for a category"""
        suggestions_map = {
            'Software': ['Audit unused subscriptions', 'Negotiate volume discounts', 'Consider annual payments'],
            'Office Supplies': ['Buy in bulk', 'Switch to generic brands', 'Implement approval workflow'],
            'Travel': ['Use corporate travel policies', 'Book in advance', 'Consider virtual meetings'],
            'Marketing': ['Focus on highest ROI channels', 'Negotiate better rates', 'Use performance-based pricing'],
            'Other': ['Review for consolidation opportunities', 'Negotiate payment terms', 'Consider alternatives']
        }
        
        return suggestions_map.get(category, suggestions_map['Other'])
    
    async def _simulate_financial_scenario(self, args: Dict) -> Dict[str, Any]:
        """Simulate different financial scenarios for testing AI responses"""
        try:
            scenario = args['scenario']
            profile = args.get('profile')
            
            if not self.use_mock_data or not self.mock_generator:
                return {'error': 'Mock data is not enabled or available'}
            
            # Change company profile if requested
            if profile and profile in DEMO_PROFILES:
                self.mock_generator = MockFinancialDataGenerator(DEMO_PROFILES[profile])
                logger.info(f"Changed financial profile to: {profile}")
            
            # Simulate the specific scenario
            scenario_data = self.mock_generator.simulate_financial_alert_scenario(scenario)
            
            # Also trigger an alert based on the scenario
            if scenario == "critical_runway":
                await self._publish_financial_alert({
                    'alert_type': 'critical_runway_simulation',
                    'scenario': scenario,
                    'runway_days': scenario_data.get('runway_days', 0),
                    'severity': 'critical',
                    'data': scenario_data,
                    'simulation': True
                })
            elif scenario == "burn_rate_spike":
                await self._publish_financial_alert({
                    'alert_type': 'burn_rate_spike_simulation',
                    'scenario': scenario,
                    'burn_rate_change': scenario_data.get('burn_rate_change_percent', 0),
                    'severity': 'high',
                    'data': scenario_data,
                    'simulation': True
                })
            elif scenario == "large_expense":
                await self._publish_financial_alert({
                    'alert_type': 'large_expense_simulation',
                    'scenario': scenario,
                    'large_expenses': scenario_data.get('large_expenses', []),
                    'severity': 'medium',
                    'data': scenario_data,
                    'simulation': True
                })
            
            return {
                'simulation_status': 'completed',
                'scenario': scenario,
                'profile_used': profile or 'current',
                'generated_data': scenario_data,
                'alert_triggered': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error simulating financial scenario: {e}")
            return {'error': str(e)}
    
    async def _publish_financial_alert(self, alert_data: Dict):
        """Publish financial alert to Redis stream"""
        try:
            await self.redis_client.xadd(
                'brex_events',
                {
                    'data': json.dumps(alert_data),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'brex_financial_monitor'
                }
            )
            logger.info(f"Published financial alert: {alert_data['alert_type']}")
        except Exception as e:
            logger.error(f"Error publishing alert: {e}")