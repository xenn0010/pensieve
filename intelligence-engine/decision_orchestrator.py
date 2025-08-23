import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

import google.generativeai as genai
from pydantic import BaseModel

from config.settings import settings
from config.supabase_client import supabase_client


class EventType(Enum):
    FINANCIAL_ALERT = "financial_alert"
    CUSTOMER_RISK = "customer_risk"
    COMPETITIVE_THREAT = "competitive_threat"
    MARKET_OPPORTUNITY = "market_opportunity"
    TECHNICAL_ISSUE = "technical_issue"


class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class IntelligenceEvent:
    event_type: EventType
    priority: Priority
    source: str
    data: Dict[str, Any]
    timestamp: datetime
    context: Optional[Dict[str, Any]] = None


class ActionDecision(BaseModel):
    action_type: str
    parameters: Dict[str, Any]
    reasoning: str
    confidence_score: float
    expected_impact: str
    urgency_level: Priority


class DecisionOrchestrator:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        self.event_queue = asyncio.Queue()
        self.active_decisions = {}
        self.decision_history = []
        
    async def start_event_processing(self):
        """Start the continuous event processing loop"""
        while True:
            try:
                # Process events from queue
                event = await asyncio.wait_for(
                    self.event_queue.get(), timeout=settings.event_processing_interval
                )
                await self._process_event(event)
            except asyncio.TimeoutError:
                # No events in queue, perform periodic intelligence gathering
                await self._periodic_intelligence_sweep()
            except Exception as e:
                print(f"Error processing event: {e}")
                
    async def add_event(self, event: IntelligenceEvent):
        """Add new intelligence event to processing queue"""
        await self.event_queue.put(event)
        
    async def _process_event(self, event: IntelligenceEvent):
        """Process individual intelligence event"""
        print(f"Processing {event.event_type.value} event from {event.source}")
        
        # Generate context-aware prompt for Gemini
        decision_prompt = self._build_decision_prompt(event)
        
        # Get AI decision
        try:
            response = await self.model.generate_content_async(decision_prompt)
            decision = self._parse_ai_decision(response.text)
            
            # Store decision in Supabase
            await supabase_client.store_ai_decision(
                decision_type=decision.action_type,
                confidence=decision.confidence_score,
                reasoning=decision.reasoning,
                action_taken=decision.parameters,
                context={
                    'event_type': event.event_type.value,
                    'event_source': event.source,
                    'event_data': event.data
                }
            )
            
            # Execute decision if confidence is high enough
            if decision.confidence_score > 0.7:
                await self._execute_decision(decision, event)
                # Log successful execution
                await supabase_client.log_business_event(
                    event_type='decision_executed',
                    event_data={
                        'decision_type': decision.action_type,
                        'confidence': decision.confidence_score,
                        'parameters': decision.parameters
                    },
                    priority='medium',
                    component='decision_orchestrator'
                )
            else:
                print(f"Low confidence decision ({decision.confidence_score}), queuing for review")
                await supabase_client.log_business_event(
                    event_type='low_confidence_decision',
                    event_data={
                        'decision_type': decision.action_type,
                        'confidence': decision.confidence_score,
                        'reasoning': decision.reasoning
                    },
                    priority='low',
                    component='decision_orchestrator'
                )
                
        except Exception as e:
            print(f"Error generating AI decision: {e}")
    
    def _build_decision_prompt(self, event: IntelligenceEvent) -> str:
        """Build comprehensive decision prompt for Gemini"""
        base_prompt = f"""
        You are an autonomous Chief Intelligence Officer for a startup. Analyze this intelligence event and decide on the optimal action.

        EVENT DETAILS:
        Type: {event.event_type.value}
        Priority: {event.priority.value}
        Source: {event.source}
        Timestamp: {event.timestamp}
        Data: {json.dumps(event.data, indent=2)}
        
        CONTEXT:
        - Company stage: Early-stage startup
        - Current financial runway: {event.context.get('runway_days', 'Unknown')} days
        - Active customer count: {event.context.get('customer_count', 'Unknown')}
        - Competitive pressure: {event.context.get('competitive_pressure', 'Unknown')}
        
        AVAILABLE ACTIONS:
        1. Financial Actions: transfer_funds, optimize_spend, emergency_funding_prep
        2. Customer Actions: escalate_support, retention_campaign, satisfaction_survey
        3. Competitive Actions: feature_gap_analysis, pricing_adjustment, market_positioning
        4. Research Actions: deep_market_analysis, competitor_intelligence, customer_research
        5. Alert Actions: notify_leadership, schedule_review, create_task
        
        Respond with a JSON object containing:
        - action_type: specific action to take
        - parameters: detailed parameters for the action
        - reasoning: detailed explanation of why this action
        - confidence_score: 0.0-1.0 confidence in this decision
        - expected_impact: predicted business impact
        - urgency_level: critical/high/medium/low
        
        Be decisive but calculated. Focus on actions that maximize business value while minimizing risk.
        """
        
        return base_prompt
    
    def _parse_ai_decision(self, response_text: str) -> ActionDecision:
        """Parse Gemini response into structured decision"""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                decision_data = json.loads(json_match.group())
                return ActionDecision(**decision_data)
        except Exception as e:
            print(f"Error parsing AI decision: {e}")
            
        # Fallback decision
        return ActionDecision(
            action_type="alert_leadership",
            parameters={"message": "AI decision parsing failed"},
            reasoning="Fallback action due to parsing error",
            confidence_score=0.3,
            expected_impact="Minimal",
            urgency_level=Priority.LOW
        )
    
    async def _execute_decision(self, decision: ActionDecision, event: IntelligenceEvent):
        """Execute the AI-generated decision"""
        print(f"Executing decision: {decision.action_type}")
        print(f"Reasoning: {decision.reasoning}")
        
        # Store decision in history
        self.decision_history.append({
            'timestamp': datetime.now(),
            'event': event,
            'decision': decision,
            'status': 'executed'
        })
        
        # Route to appropriate action executor
        if decision.action_type.startswith('financial_'):
            await self._execute_financial_action(decision)
        elif decision.action_type.startswith('customer_'):
            await self._execute_customer_action(decision)
        elif decision.action_type.startswith('competitive_'):
            await self._execute_competitive_action(decision)
        else:
            print(f"Unknown action type: {decision.action_type}")
    
    async def _execute_financial_action(self, decision: ActionDecision):
        """Execute financial-related actions"""
        # Implementation will integrate with Brex MCP server
        print(f"Would execute financial action: {decision.parameters}")
        
    async def _execute_customer_action(self, decision: ActionDecision):
        """Execute customer-related actions"""
        # Implementation will integrate with Pylon MCP server
        print(f"Would execute customer action: {decision.parameters}")
        
    async def _execute_competitive_action(self, decision: ActionDecision):
        """Execute competitive intelligence actions"""
        # Implementation will integrate with SixtyFour/MixRank MCP servers
        print(f"Would execute competitive action: {decision.parameters}")
        
    async def _periodic_intelligence_sweep(self):
        """Perform periodic intelligence gathering when no events are queued"""
        print("Performing periodic intelligence sweep...")
        
        # Coordinate WOW intelligence analysis across all MCP servers
        await self._coordinate_wow_intelligence_analysis()
        
    async def _coordinate_wow_intelligence_analysis(self):
        """Coordinate comprehensive WOW intelligence analysis across all systems"""
        try:
            # Define target companies for intelligence analysis
            target_companies = [
                'competitor1.com',
                'competitor2.com', 
                'unicorn-startup.com',
                'legacy-enterprise.com'
            ]
            
            intelligence_results = {}
            
            # Gather intelligence from all sources
            for company in target_companies:
                print(f"Running comprehensive WOW intelligence analysis for {company}")
                
                # Collect intelligence from all MCP servers simultaneously
                intelligence_tasks = []
                
                # Task 1: SixtyFour people & market intelligence
                intelligence_tasks.append(
                    self._analyze_sixtyfour_wow_intelligence(company)
                )
                
                # Task 2: MixRank technology intelligence  
                intelligence_tasks.append(
                    self._analyze_mixrank_tech_intelligence(company)
                )
                
                # Task 3: Financial intelligence (Brex mock data)
                intelligence_tasks.append(
                    self._analyze_financial_intelligence(company)
                )
                
                # Execute all intelligence gathering simultaneously
                results = await asyncio.gather(*intelligence_tasks, return_exceptions=True)
                
                # Compile results
                intelligence_results[company] = {
                    'sixtyfour_intelligence': results[0] if len(results) > 0 else {},
                    'mixrank_intelligence': results[1] if len(results) > 1 else {},
                    'financial_intelligence': results[2] if len(results) > 2 else {},
                    'analysis_timestamp': datetime.now().isoformat()
                }
                
                # Process combined intelligence for this company
                await self._process_combined_intelligence(company, intelligence_results[company])
            
            # Store comprehensive intelligence analysis
            await supabase_client.log_business_event(
                event_type='comprehensive_wow_intelligence_analysis',
                event_data={
                    'companies_analyzed': len(target_companies),
                    'total_signals_detected': sum(
                        len(data.get('sixtyfour_intelligence', {}).get('wow_signals', [])) +
                        len(data.get('mixrank_intelligence', {}).get('technology_wow_signals', []))
                        for data in intelligence_results.values()
                    ),
                    'analysis_summary': intelligence_results
                },
                priority='medium',
                component='decision_orchestrator'
            )
            
        except Exception as e:
            print(f"Error in WOW intelligence analysis coordination: {e}")
            await supabase_client.log_business_event(
                event_type='intelligence_analysis_error',
                event_data={'error': str(e)},
                priority='high',
                component='decision_orchestrator'
            )
    
    async def _analyze_sixtyfour_wow_intelligence(self, company_domain: str) -> Dict[str, Any]:
        """Mock SixtyFour WOW intelligence analysis (would integrate with actual MCP server)"""
        try:
            # This would integrate with the actual SixtyFour MCP server
            # For now, simulate the analysis with the same logic
            from mcp_servers.sixtyfour_mcp.market_intelligence import SixtyFourMarketIntelligence
            
            sixtyfour = SixtyFourMarketIntelligence()
            return await sixtyfour.analyze_wow_intelligence_signals(company_domain)
        except Exception as e:
            print(f"Error analyzing SixtyFour intelligence for {company_domain}: {e}")
            return {'error': str(e)}
    
    async def _analyze_mixrank_tech_intelligence(self, company_domain: str) -> Dict[str, Any]:
        """Mock MixRank technology intelligence analysis (would integrate with actual MCP server)"""
        try:
            # This would integrate with the actual MixRank MCP server
            from mcp_servers.mixrank_mcp.technology_intelligence import MixRankTechnologyIntelligence
            
            mixrank = MixRankTechnologyIntelligence()
            return await mixrank.analyze_technology_wow_signals(company_domain)
        except Exception as e:
            print(f"Error analyzing MixRank intelligence for {company_domain}: {e}")
            return {'error': str(e)}
    
    async def _analyze_financial_intelligence(self, company_domain: str) -> Dict[str, Any]:
        """Analyze financial intelligence patterns"""
        try:
            # This would integrate with the Brex MCP server
            from mcp_servers.brex_mcp.financial_monitor import BrexFinancialMonitor
            
            brex = BrexFinancialMonitor()
            # Generate mock financial analysis for the company
            return {
                'company_domain': company_domain,
                'financial_health_score': 0.75,
                'burn_rate_trend': 'stable',
                'cash_runway_days': 180,
                'financial_risk_signals': [],
                'analysis_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error analyzing financial intelligence for {company_domain}: {e}")
            return {'error': str(e)}
    
    async def _process_combined_intelligence(self, company_domain: str, intelligence_data: Dict[str, Any]):
        """Process combined intelligence data and generate autonomous actions"""
        try:
            # Extract all WOW signals detected
            all_wow_signals = []
            
            sixtyfour_data = intelligence_data.get('sixtyfour_intelligence', {})
            if 'wow_signals' in sixtyfour_data:
                all_wow_signals.extend(sixtyfour_data['wow_signals'])
            
            mixrank_data = intelligence_data.get('mixrank_intelligence', {})
            if 'technology_wow_signals' in mixrank_data:
                all_wow_signals.extend(mixrank_data['technology_wow_signals'])
            
            # If we detected significant WOW signals, create an intelligence event
            if all_wow_signals:
                critical_signals = [s for s in all_wow_signals if s.get('severity') == 'critical']
                high_signals = [s for s in all_wow_signals if s.get('severity') == 'high']
                
                if critical_signals or len(high_signals) >= 2:
                    # Create high-priority intelligence event
                    event = IntelligenceEvent(
                        event_type=EventType.COMPETITIVE_THREAT if critical_signals else EventType.MARKET_OPPORTUNITY,
                        priority=Priority.CRITICAL if critical_signals else Priority.HIGH,
                        source='wow_intelligence_orchestrator',
                        data={
                            'company_analyzed': company_domain,
                            'total_signals': len(all_wow_signals),
                            'critical_signals': len(critical_signals),
                            'high_signals': len(high_signals),
                            'wow_signals_detected': all_wow_signals[:5],  # Top 5 signals
                            'recommended_actions': self._compile_wow_recommended_actions(all_wow_signals),
                            'estimated_impact': self._estimate_combined_impact(all_wow_signals)
                        },
                        timestamp=datetime.now(),
                        context={
                            'intelligence_type': 'wow_signal_analysis',
                            'analysis_scope': 'comprehensive_multi_domain',
                            'target_company': company_domain
                        }
                    )
                    
                    # Add to processing queue
                    await self.add_event(event)
                    
                    print(f"Generated high-priority WOW intelligence event for {company_domain}")
                    print(f"Detected {len(critical_signals)} critical and {len(high_signals)} high-severity signals")
        
        except Exception as e:
            print(f"Error processing combined intelligence for {company_domain}: {e}")
    
    def _compile_wow_recommended_actions(self, wow_signals: List[Dict[str, Any]]) -> List[str]:
        """Compile recommended actions from all WOW signals"""
        actions = set()  # Use set to avoid duplicates
        
        signal_types = {s.get('signal_type') for s in wow_signals}
        
        # Financial distress signals
        if any('exodus' in st or 'death' in st for st in signal_types):
            actions.update([
                'Monitor for acquisition opportunities at distressed valuations',
                'Review vendor relationships with distressed companies',
                'Prepare competitive recruitment from struggling competitors'
            ])
        
        # Technology advantage signals
        if any('ai' in st or 'stealth' in st for st in signal_types):
            actions.update([
                'Accelerate AI capability development to maintain competitiveness',
                'Investigate potential technology partnerships',
                'Review AI talent acquisition strategy'
            ])
        
        # Regulatory and compliance signals
        if any('privacy' in st or 'regulatory' in st for st in signal_types):
            actions.update([
                'Review compliance posture and privacy practices',
                'Assess competitive advantage from superior compliance',
                'Monitor regulatory changes for market opportunities'
            ])
        
        # Market manipulation and fraud signals
        if any('manipulation' in st or 'scandal' in st for st in signal_types):
            actions.update([
                'Maintain ethical business practices for competitive advantage',
                'Monitor market conditions for irregularities',
                'Prepare for potential market disruption'
            ])
        
        return list(actions)[:8]  # Top 8 actions
    
    def _estimate_combined_impact(self, wow_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate combined business impact of all WOW signals"""
        impact_scores = []
        cost_impacts = []
        timeline_impacts = []
        
        for signal in wow_signals:
            # Extract impact metrics
            if 'probability' in str(signal):
                for key, value in signal.items():
                    if 'probability' in key and isinstance(value, (int, float)):
                        impact_scores.append(value / 100)  # Normalize to 0-1
            
            if 'cost_impact_millions' in signal:
                cost_impacts.append(signal['cost_impact_millions'])
            
            if 'timeline_months' in str(signal):
                for key, value in signal.items():
                    if 'timeline' in key and isinstance(value, (int, float)):
                        timeline_impacts.append(value)
        
        return {
            'average_impact_probability': sum(impact_scores) / len(impact_scores) if impact_scores else 0,
            'total_estimated_cost_impact_millions': sum(cost_impacts),
            'average_timeline_months': sum(timeline_impacts) / len(timeline_impacts) if timeline_impacts else 0,
            'overall_threat_level': 'high' if any(s.get('severity') == 'critical' for s in wow_signals) else 'medium'
        }