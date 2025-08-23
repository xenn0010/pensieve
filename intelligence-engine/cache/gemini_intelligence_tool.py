"""
Gemini Tool for Instant Intelligence Access

Provides Gemini with instant access to cached company intelligence data.
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime

from config.logging_config import get_component_logger
from .intelligence_cache_manager import cache_manager

logger = get_component_logger("gemini_intelligence_tool")


class GeminiIntelligenceTool:
    """Tool that Gemini can use to access cached company intelligence"""
    
    def __init__(self):
        self.logger = get_component_logger("gemini_intelligence_tool")
    
    async def get_company_intelligence(
        self, 
        company_name: str, 
        research_depth: str = 'standard',
        intelligence_type: str = 'competitive'
    ) -> Dict[str, Any]:
        """
        Tool function for Gemini to get company intelligence data.
        
        Args:
            company_name: Name of the company to analyze
            research_depth: 'basic', 'standard', or 'maximum'
            intelligence_type: 'competitive', 'financial', or 'strategic'
        
        Returns:
            Dictionary with intelligence data or cache miss info
        """
        
        self.logger.info(f"Gemini requesting intelligence: {company_name} ({intelligence_type}, {research_depth})")
        
        # Try to get from cache
        intelligence_data = await cache_manager.get_intelligence(
            company_name, research_depth, intelligence_type
        )
        
        if intelligence_data:
            # Cache hit - return formatted data for Gemini
            return {
                'status': 'success',
                'company': company_name,
                'research_depth': research_depth,
                'intelligence_type': intelligence_type,
                'cache_hit': True,
                'data': intelligence_data,
                'summary': self._generate_intelligence_summary(intelligence_data)
            }
        else:
            # Cache miss - data is being fetched
            return {
                'status': 'cache_miss',
                'company': company_name,
                'research_depth': research_depth,
                'intelligence_type': intelligence_type,
                'cache_hit': False,
                'message': f'Intelligence for {company_name} is being fetched. Try again in a few minutes.',
                'estimated_ready_time': '5-10 minutes for deep intelligence'
            }
    
    def _generate_intelligence_summary(self, data: Dict[str, Any]) -> str:
        """Generate a concise summary for Gemini to use in reasoning"""
        
        summary_parts = []
        
        # Financial health summary
        if data.get('financial_health'):
            fh = str(data['financial_health'])[:200]
            summary_parts.append(f"Financial: {fh}")
        
        # Competitive signals summary  
        if data.get('competitive_signals'):
            cs = str(data['competitive_signals'])[:200]
            summary_parts.append(f"Competitive: {cs}")
        
        # Strategic shifts summary
        if data.get('strategic_shifts'):
            ss = str(data['strategic_shifts'])[:200]
            summary_parts.append(f"Strategy: {ss}")
        
        # Market opportunities summary
        if data.get('market_opportunities'):
            mo = str(data['market_opportunities'])[:200]
            summary_parts.append(f"Opportunities: {mo}")
        
        return " | ".join(summary_parts)
    
    async def search_companies_by_criteria(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search cached companies by specific criteria.
        
        Args:
            criteria: Search criteria like {'financial_health': 'strong', 'market_opportunities': 'high'}
        
        Returns:
            List of companies matching criteria
        """
        
        # This would query the cache database for companies matching criteria
        # For now, return a simple implementation
        return [
            {
                'company': 'stripe',
                'match_score': 0.95,
                'reasons': ['Strong financial health', 'High market opportunities']
            }
        ]
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get the tool definition for Gemini function calling"""
        
        return {
            "name": "get_company_intelligence",
            "description": "Get comprehensive intelligence data about a company including financial health, competitive signals, strategic shifts, and market opportunities. Data is instantly available from cache.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "Name of the company to analyze (e.g., 'stripe', 'openai', 'github')"
                    },
                    "research_depth": {
                        "type": "string",
                        "enum": ["basic", "standard", "maximum"],
                        "description": "Depth of research - basic (1 day cache), standard (12 hour cache), maximum (6 hour cache)",
                        "default": "standard"
                    },
                    "intelligence_type": {
                        "type": "string", 
                        "enum": ["competitive", "financial", "strategic"],
                        "description": "Type of intelligence focus - competitive analysis, financial health, or strategic insights",
                        "default": "competitive"
                    }
                },
                "required": ["company_name"]
            }
        }


# Tool for Gemini prompt integration
GEMINI_INTELLIGENCE_PROMPT = """
You have access to a powerful company intelligence tool that provides real-time business intelligence data.

TOOL: get_company_intelligence(company_name, research_depth='standard', intelligence_type='competitive')

This tool gives you instant access to:
- **Financial Health**: Cash flow patterns, hiring velocity, payment behaviors
- **Competitive Signals**: Market position, customer migration, pricing intelligence  
- **Strategic Shifts**: Product pivots, market repositioning, technology adoption
- **Customer Intelligence**: Expansion patterns, integration depth, renewal risks
- **Market Opportunities**: Growth areas, acquisition targets, market gaps

USAGE EXAMPLES:
- get_company_intelligence("stripe", "maximum", "competitive")
- get_company_intelligence("openai", "standard", "financial") 
- get_company_intelligence("github", "basic", "strategic")

RESEARCH DEPTHS:
- **basic**: High-level overview (24h cache)
- **standard**: Comprehensive analysis (12h cache) 
- **maximum**: Deep intelligence gathering (6h cache)

INTELLIGENCE TYPES:
- **competitive**: Market position, competitive threats, customer dynamics
- **financial**: Cash flow, burn rate, financial health indicators
- **strategic**: Business model shifts, strategic partnerships, pivot signals

Use this tool whenever you need to make informed decisions about companies, competitive analysis, investment decisions, or strategic planning.
"""


# Global tool instance
gemini_intelligence_tool = GeminiIntelligenceTool()
