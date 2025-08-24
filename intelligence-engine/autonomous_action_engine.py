#!/usr/bin/env python3
"""
Autonomous Action Execution Engine
Enables Gemini AI to execute business actions autonomously
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

from config.settings import settings
from config.supabase_client import supabase_client

logger = logging.getLogger(__name__)


class ActionType(Enum):
    FINANCIAL = "financial"
    COMPETITIVE = "competitive"
    CUSTOMER = "customer"
    OPERATIONAL = "operational"
    COMMUNICATION = "communication"


class ExecutionMode(Enum):
    AUTONOMOUS = "autonomous"    # Execute immediately
    ADVISORY = "advisory"       # Generate recommendation
    ALERT = "alert"            # Alert only


@dataclass
class ActionResult:
    action_id: str
    success: bool
    execution_time: datetime
    result_data: Dict[str, Any]
    error_message: Optional[str] = None
    impact_score: Optional[float] = None


class AutonomousActionEngine:
    def __init__(self):
        self.active_actions = {}
        self.action_history = []
        self.tool_registry = {}
        self.confidence_thresholds = {
            "autonomous": 0.8,
            "advisory": 0.6,
            "alert": 0.4
        }
        
    async def initialize(self):
        """Initialize the autonomous action engine"""
        await self._register_all_tools()
        logger.info("Autonomous Action Engine initialized with tools")
        
    async def _register_all_tools(self):
        """Register all available tools for Gemini access"""
        from .tools.financial_actions import FinancialActionTools
        from .tools.competitive_actions import CompetitiveActionTools
        from .tools.customer_actions import CustomerActionTools
        from .tools.operational_actions import OperationalActionTools
        from .tools.communication_actions import CommunicationActionTools
        
        self.tool_registry = {
            ActionType.FINANCIAL: FinancialActionTools(),
            ActionType.COMPETITIVE: CompetitiveActionTools(),
            ActionType.CUSTOMER: CustomerActionTools(),
            ActionType.OPERATIONAL: OperationalActionTools(),
            ActionType.COMMUNICATION: CommunicationActionTools()
        }
        
        logger.info(f"Registered {len(self.tool_registry)} action tool categories")
    
    async def execute_autonomous_action(self, intelligence_event: Dict[str, Any]) -> ActionResult:
        """Execute autonomous action based on intelligence event"""
        try:
            # Determine action type and confidence
            action_type = self._determine_action_type(intelligence_event)
            confidence = intelligence_event.get('confidence', 0.5)
            execution_mode = self._determine_execution_mode(confidence)
            
            # Generate action plan
            action_plan = await self._generate_action_plan(intelligence_event, action_type)
            
            if execution_mode == ExecutionMode.AUTONOMOUS:
                # Execute immediately
                result = await self._execute_action_plan(action_plan)
                
                # Log to Supabase
                await self._log_autonomous_action(intelligence_event, action_plan, result)
                
                return result
                
            elif execution_mode == ExecutionMode.ADVISORY:
                # Generate recommendation for human approval
                recommendation = await self._generate_recommendation(action_plan)
                return ActionResult(
                    action_id=action_plan['id'],
                    success=True,
                    execution_time=datetime.now(),
                    result_data={"recommendation": recommendation, "requires_approval": True}
                )
                
            else:  # ALERT mode
                # Generate alert only
                alert = await self._generate_alert(intelligence_event)
                return ActionResult(
                    action_id=f"alert_{datetime.now().timestamp()}",
                    success=True,
                    execution_time=datetime.now(),
                    result_data={"alert": alert, "action": "monitoring_only"}
                )
                
        except Exception as e:
            logger.error(f"Error executing autonomous action: {e}")
            return ActionResult(
                action_id="error",
                success=False,
                execution_time=datetime.now(),
                result_data={},
                error_message=str(e)
            )
    
    def _determine_action_type(self, intelligence_event: Dict[str, Any]) -> ActionType:
        """Determine the type of action needed based on intelligence event"""
        event_type = intelligence_event.get('event_type', '')
        signal_types = [s.get('signal_type', '') for s in intelligence_event.get('wow_signals', [])]
        
        # Financial distress signals
        if any('exodus' in s or 'death' in s or 'cash' in s for s in signal_types):
            return ActionType.FINANCIAL
            
        # Competitive threat signals
        elif any('acquisition' in s or 'competitive' in s or 'talent_war' in s for s in signal_types):
            return ActionType.COMPETITIVE
            
        # Customer-related signals
        elif any('churn' in s or 'satisfaction' in s for s in signal_types):
            return ActionType.CUSTOMER
            
        # Communication/PR signals
        elif any('scandal' in s or 'regulatory' in s or 'manipulation' in s for s in signal_types):
            return ActionType.COMMUNICATION
            
        # Default to operational
        else:
            return ActionType.OPERATIONAL
    
    def _determine_execution_mode(self, confidence: float) -> ExecutionMode:
        """Determine execution mode based on confidence score"""
        if confidence >= self.confidence_thresholds["autonomous"]:
            return ExecutionMode.AUTONOMOUS
        elif confidence >= self.confidence_thresholds["advisory"]:
            return ExecutionMode.ADVISORY
        else:
            return ExecutionMode.ALERT
    
    async def _generate_action_plan(self, intelligence_event: Dict[str, Any], action_type: ActionType) -> Dict[str, Any]:
        """Generate detailed action plan using appropriate tools"""
        tool_set = self.tool_registry[action_type]
        
        # Use tool set to generate plan
        action_plan = await tool_set.generate_action_plan(intelligence_event)
        
        return {
            "id": f"action_{datetime.now().timestamp()}",
            "type": action_type.value,
            "confidence": intelligence_event.get('confidence', 0.5),
            "trigger_event": intelligence_event,
            "actions": action_plan,
            "estimated_impact": await tool_set.estimate_impact(action_plan),
            "execution_timeline": await tool_set.get_execution_timeline(action_plan),
            "created_at": datetime.now().isoformat()
        }
    
    async def _execute_action_plan(self, action_plan: Dict[str, Any]) -> ActionResult:
        """Execute the action plan"""
        try:
            action_type = ActionType(action_plan['type'])
            tool_set = self.tool_registry[action_type]
            
            # Execute all actions in the plan
            execution_results = []
            for action in action_plan['actions']:
                result = await tool_set.execute_action(action)
                execution_results.append(result)
            
            # Calculate overall success
            success_rate = sum(1 for r in execution_results if r.get('success', False)) / len(execution_results)
            
            return ActionResult(
                action_id=action_plan['id'],
                success=success_rate > 0.7,  # 70% success threshold
                execution_time=datetime.now(),
                result_data={
                    "action_results": execution_results,
                    "success_rate": success_rate,
                    "actions_executed": len(execution_results)
                },
                impact_score=action_plan.get('estimated_impact', {}).get('score', 0.5)
            )
            
        except Exception as e:
            logger.error(f"Error executing action plan: {e}")
            return ActionResult(
                action_id=action_plan['id'],
                success=False,
                execution_time=datetime.now(),
                result_data={},
                error_message=str(e)
            )
    
    async def _generate_recommendation(self, action_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate human-readable recommendation"""
        return {
            "title": f"Recommended Action: {action_plan['type'].title()} Response",
            "description": f"Based on {len(action_plan.get('actions', []))} proposed actions",
            "confidence": action_plan['confidence'],
            "estimated_impact": action_plan.get('estimated_impact', {}),
            "timeline": action_plan.get('execution_timeline', "immediate"),
            "actions_summary": [
                action.get('description', action.get('type', 'Unknown action'))
                for action in action_plan.get('actions', [])
            ],
            "approval_required": True,
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
    
    async def _generate_alert(self, intelligence_event: Dict[str, Any]) -> Dict[str, Any]:
        """Generate alert for low-confidence events"""
        return {
            "title": f"Intelligence Alert: {intelligence_event.get('event_type', 'Unknown Event')}",
            "description": "Low confidence signal detected, monitoring recommended",
            "signals_detected": len(intelligence_event.get('wow_signals', [])),
            "risk_level": intelligence_event.get('risk_level', 'unknown'),
            "monitoring_urgency": intelligence_event.get('monitoring_urgency', 'standard'),
            "recommended_actions": intelligence_event.get('recommended_actions', []),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _log_autonomous_action(self, intelligence_event: Dict[str, Any], action_plan: Dict[str, Any], result: ActionResult):
        """Log autonomous action to Supabase"""
        try:
            await supabase_client.store_ai_decision(
                decision_type=f"autonomous_{action_plan['type']}",
                confidence=action_plan['confidence'],
                reasoning=f"Autonomous response to {intelligence_event.get('event_type', 'intelligence_event')}",
                action_taken={
                    "action_plan": action_plan,
                    "execution_result": {
                        "success": result.success,
                        "impact_score": result.impact_score,
                        "result_data": result.result_data
                    }
                },
                context={
                    "trigger_event": intelligence_event,
                    "execution_mode": "autonomous",
                    "tool_type": action_plan['type']
                }
            )
            
            # Also log as business event
            await supabase_client.log_business_event(
                event_type='autonomous_action_executed',
                event_data={
                    "action_id": result.action_id,
                    "action_type": action_plan['type'],
                    "success": result.success,
                    "impact_score": result.impact_score
                },
                priority='high' if result.impact_score and result.impact_score > 0.7 else 'medium',
                component='autonomous_action_engine'
            )
            
        except Exception as e:
            logger.error(f"Error logging autonomous action: {e}")
    
    async def get_available_tools(self, action_type: Optional[ActionType] = None) -> Dict[str, List[str]]:
        """Get list of available tools for Gemini"""
        if action_type:
            tool_set = self.tool_registry[action_type]
            return {action_type.value: await tool_set.list_available_tools()}
        else:
            all_tools = {}
            for action_type, tool_set in self.tool_registry.items():
                all_tools[action_type.value] = await tool_set.list_available_tools()
            return all_tools
    
    async def execute_specific_tool(self, action_type: str, tool_name: str, parameters: Dict[str, Any]) -> ActionResult:
        """Execute a specific tool with given parameters"""
        try:
            tool_set = self.tool_registry[ActionType(action_type)]
            result = await tool_set.execute_specific_tool(tool_name, parameters)
            
            return ActionResult(
                action_id=f"{action_type}_{tool_name}_{datetime.now().timestamp()}",
                success=result.get('success', False),
                execution_time=datetime.now(),
                result_data=result,
                impact_score=result.get('impact_score', 0.5)
            )
            
        except Exception as e:
            logger.error(f"Error executing specific tool {tool_name}: {e}")
            return ActionResult(
                action_id="error",
                success=False,
                execution_time=datetime.now(),
                result_data={},
                error_message=str(e)
            )
    
    async def get_action_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent action history"""
        return self.action_history[-limit:] if self.action_history else []
    
    async def get_active_actions(self) -> Dict[str, Any]:
        """Get currently active/pending actions"""
        return self.active_actions