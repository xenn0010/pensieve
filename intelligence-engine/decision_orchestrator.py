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
        # This will trigger data collection from all MCP servers