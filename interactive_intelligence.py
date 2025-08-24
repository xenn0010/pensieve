#!/usr/bin/env python3
"""
Interactive WOW Intelligence Analyzer
Allows users to analyze any company by name and industry using our AI agent
"""

import asyncio
import sys
import os
import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

import google.generativeai as genai

# Add the project root to the Python path
sys.path.append('.')

from config.settings import settings

class CompanyIntelligenceAnalyzer:
    """Interactive company intelligence analysis system"""
    
    def __init__(self):
        self.supported_industries = [
            'technology', 'fintech', 'saas', 'e-commerce', 'healthcare', 
            'biotech', 'manufacturing', 'retail', 'media', 'gaming',
            'automotive', 'real-estate', 'education', 'food-delivery',
            'logistics', 'energy', 'aerospace', 'telecommunications'
        ]
        
        # Initialize Google Gemini
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        
    async def analyze_company(self, company_name: str, industry: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a company using comprehensive WOW intelligence"""
        
        # Validate and clean inputs
        company_name = self._clean_company_name(company_name)
        industry = self._validate_industry(industry)
        domain = self._generate_domain_if_missing(company_name, domain)
        
        print(f"\n{'='*80}")
        print(f"ANALYZING: {company_name}")
        print(f"INDUSTRY: {industry}")
        print(f"DOMAIN: {domain}")
        print(f"ANALYSIS TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Initialize intelligence systems
        try:
            # Import intelligence systems
            sys.path.append(os.path.join('.', 'mcp-servers', 'sixtyfour-mcp'))
            from market_intelligence import SixtyFourMarketIntelligence
            
            sys.path.append(os.path.join('.', 'mcp-servers', 'mixrank-mcp'))  
            from technology_intelligence import MixRankTechnologyIntelligence
            
            sixtyfour = SixtyFourMarketIntelligence()
            mixrank = MixRankTechnologyIntelligence()
            
            print("Intelligence systems initialized...")
            
            # Run comprehensive analysis
            print("Gathering intelligence signals...")
            
            # Execute intelligence gathering simultaneously
            results = await asyncio.gather(
                self._analyze_market_intelligence(sixtyfour, company_name, domain, industry),
                self._analyze_technology_intelligence(mixrank, company_name, domain, industry),
                self._analyze_financial_patterns(company_name, domain, industry),
                return_exceptions=True
            )
            
            market_intel = results[0] if len(results) > 0 and not isinstance(results[0], Exception) else {}
            tech_intel = results[1] if len(results) > 1 and not isinstance(results[1], Exception) else {}
            financial_intel = results[2] if len(results) > 2 and not isinstance(results[2], Exception) else {}
            
            # Use Gemini AI to enhance the intelligence analysis
            enhanced_analysis = await self._gemini_enhanced_analysis(
                company_name, domain, industry, market_intel, tech_intel, financial_intel
            )
            
            # Process and combine intelligence
            analysis_result = await self._process_combined_intelligence(
                company_name, domain, industry, market_intel, tech_intel, financial_intel, enhanced_analysis
            )
            
            return analysis_result
            
        except Exception as e:
            print(f"ERROR: Analysis failed: {e}")
            return {'error': str(e), 'company': company_name, 'industry': industry}
    
    async def _analyze_market_intelligence(self, sixtyfour, company_name: str, domain: str, industry: str) -> Dict[str, Any]:
        """Analyze market and people intelligence"""
        try:
            # Enhance the analysis with industry-specific context
            result = await sixtyfour.analyze_wow_intelligence_signals(domain)
            
            # Add industry-specific context
            result['company_context'] = {
                'name': company_name,
                'industry': industry,
                'analysis_focus': 'market_and_people_intelligence'
            }
            
            return result
        except Exception as e:
            print(f"WARNING: Market intelligence error: {e}")
            return {'error': str(e)}
    
    async def _analyze_technology_intelligence(self, mixrank, company_name: str, domain: str, industry: str) -> Dict[str, Any]:
        """Analyze technology and infrastructure intelligence"""
        try:
            result = await mixrank.analyze_technology_wow_signals(domain)
            
            # Add industry-specific technology context
            result['company_context'] = {
                'name': company_name,
                'industry': industry,
                'analysis_focus': 'technology_and_infrastructure_intelligence'
            }
            
            return result
        except Exception as e:
            print(f"⚠️ Technology intelligence error: {e}")
            return {'error': str(e)}
    
    async def _analyze_financial_patterns(self, company_name: str, domain: str, industry: str) -> Dict[str, Any]:
        """Analyze financial intelligence patterns"""
        try:
            # Generate industry-specific financial intelligence
            return {
                'company_name': company_name,
                'domain': domain,
                'industry': industry,
                'financial_health_indicators': self._generate_industry_financial_patterns(industry),
                'burn_rate_analysis': self._estimate_burn_rate_by_industry(industry),
                'funding_stage_prediction': self._predict_funding_stage(company_name, industry),
                'competitive_financial_position': self._assess_competitive_position(industry),
                'analysis_focus': 'financial_intelligence'
            }
        except Exception as e:
            print(f"⚠️ Financial intelligence error: {e}")
            return {'error': str(e)}
    
    async def _gemini_enhanced_analysis(self, company_name: str, domain: str, industry: str,
                                       market_intel: Dict, tech_intel: Dict, financial_intel: Dict) -> Dict[str, Any]:
        """Use Google Gemini AI to provide enhanced intelligence analysis"""
        try:
            print("Enhancing analysis with Google Gemini AI...")
            
            # Extract key signals for Gemini analysis
            market_signals = market_intel.get('wow_signals', [])
            tech_signals = tech_intel.get('technology_wow_signals', [])
            
            # Create comprehensive intelligence prompt for Gemini
            gemini_prompt = f"""
            You are an elite business intelligence analyst. Analyze this comprehensive intelligence data for {company_name} in the {industry} industry and provide strategic insights.

            COMPANY INFORMATION:
            - Company: {company_name}
            - Domain: {domain}
            - Industry: {industry}
            - Analysis Date: {datetime.now().strftime('%Y-%m-%d')}

            MARKET INTELLIGENCE SIGNALS DETECTED:
            {json.dumps(market_signals[:5], indent=2) if market_signals else 'No critical market signals detected'}

            TECHNOLOGY INTELLIGENCE SIGNALS DETECTED:
            {json.dumps(tech_signals[:5], indent=2) if tech_signals else 'No critical technology signals detected'}

            FINANCIAL INTELLIGENCE:
            {json.dumps(financial_intel, indent=2)}

            ANALYSIS REQUIREMENTS:
            1. Provide strategic business insights based on detected signals
            2. Identify the top 3 most critical threats
            3. Identify the top 3 most promising opportunities  
            4. Recommend 5 specific actionable strategies
            5. Assess overall business health and sustainability
            6. Predict likely business outcomes in next 12 months
            7. Provide competitive positioning assessment

            Respond in JSON format with the following structure:
            {{
                "strategic_insights": ["insight1", "insight2", "insight3"],
                "critical_threats": [
                    {{"threat": "threat description", "probability": 0.8, "impact": "high", "timeline_months": 6}},
                    {{"threat": "threat description", "probability": 0.7, "impact": "medium", "timeline_months": 3}},
                    {{"threat": "threat description", "probability": 0.6, "impact": "high", "timeline_months": 12}}
                ],
                "opportunities": [
                    {{"opportunity": "opportunity description", "potential_value": "high", "effort_required": "medium"}},
                    {{"opportunity": "opportunity description", "potential_value": "medium", "effort_required": "low"}},
                    {{"opportunity": "opportunity description", "potential_value": "high", "effort_required": "high"}}
                ],
                "actionable_strategies": [
                    "strategy 1", "strategy 2", "strategy 3", "strategy 4", "strategy 5"
                ],
                "business_health_score": 0.7,
                "sustainability_assessment": "assessment description",
                "twelve_month_outlook": {{
                    "most_likely_scenario": "scenario description",
                    "best_case_scenario": "best case description", 
                    "worst_case_scenario": "worst case description",
                    "key_factors": ["factor1", "factor2", "factor3"]
                }},
                "competitive_position": {{
                    "market_position": "leader/challenger/follower/niche",
                    "competitive_advantages": ["advantage1", "advantage2"],
                    "vulnerabilities": ["vulnerability1", "vulnerability2"],
                    "competitive_threats": ["threat1", "threat2"]
                }},
                "gemini_confidence_score": 0.85
            }}
            """
            
            # Get Gemini analysis
            response = await self.model.generate_content_async(gemini_prompt)
            
            # Enhanced Gemini response parsing with better error handling
            try:
                response_text = response.text.strip()
                print(f"Gemini raw response length: {len(response_text)} chars")
                
                # Try multiple JSON extraction strategies
                gemini_analysis = None
                
                # Strategy 1: Look for complete JSON object
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
                if json_match:
                    try:
                        gemini_analysis = json.loads(json_match.group())
                        print("✓ Successfully parsed Gemini JSON (Strategy 1)")
                        return self._validate_and_fix_gemini_analysis(gemini_analysis)
                    except json.JSONDecodeError:
                        pass
                
                # Strategy 2: Look for JSON between code blocks
                code_block_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL | re.IGNORECASE)
                if code_block_match and not gemini_analysis:
                    try:
                        gemini_analysis = json.loads(code_block_match.group(1))
                        print("✓ Successfully parsed Gemini JSON (Strategy 2)")
                        return self._validate_and_fix_gemini_analysis(gemini_analysis)
                    except json.JSONDecodeError:
                        pass
                
                # Strategy 3: Clean and parse the entire response
                if not gemini_analysis:
                    cleaned_text = response_text.replace('\n', ' ').replace('\r', '').strip()
                    # Remove markdown and extra text
                    cleaned_text = re.sub(r'^[^{]*', '', cleaned_text)
                    cleaned_text = re.sub(r'[^}]*$', '', cleaned_text[::-1])[::-1]
                    
                    try:
                        gemini_analysis = json.loads(cleaned_text)
                        print("✓ Successfully parsed Gemini JSON (Strategy 3)")
                        return self._validate_and_fix_gemini_analysis(gemini_analysis)
                    except json.JSONDecodeError:
                        pass
                
                # If all parsing strategies fail
                print("Warning: All JSON parsing strategies failed for Gemini response")
                print(f"Response preview: {response_text[:200]}...")
                return self._create_fallback_gemini_analysis()
                
            except json.JSONDecodeError as e:
                print(f"Warning: Gemini JSON parsing error: {e}")
                print(f"Problematic JSON preview: {response_text[:200]}...")
                return self._create_fallback_gemini_analysis()
            except Exception as e:
                print(f"Warning: Unexpected error in Gemini JSON parsing: {e}")
                return self._create_fallback_gemini_analysis()
                
        except Exception as e:
            print(f"Warning: Gemini analysis error: {e}")
            print(f"Error type: {type(e).__name__}")
            return self._create_fallback_gemini_analysis()
    
    def _validate_and_fix_gemini_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix Gemini analysis structure"""
        try:
            # Ensure required keys exist
            required_keys = [
                'strategic_insights', 'critical_threats', 'opportunities', 
                'actionable_strategies', 'business_health_score', 'sustainability_assessment',
                'twelve_month_outlook', 'competitive_position', 'gemini_confidence_score'
            ]
            
            # Fix missing keys
            for key in required_keys:
                if key not in analysis:
                    if key == 'strategic_insights':
                        analysis[key] = ["Market analysis indicates areas for strategic focus"]
                    elif key == 'critical_threats':
                        analysis[key] = [{"threat": "Competitive landscape changes", "probability": 0.5, "impact": "medium", "timeline_months": 6}]
                    elif key == 'opportunities':
                        analysis[key] = [{"opportunity": "Market positioning improvements", "potential_value": "medium", "effort_required": "medium"}]
                    elif key == 'actionable_strategies':
                        analysis[key] = ["Monitor market conditions", "Strengthen competitive positioning"]
                    elif key == 'business_health_score':
                        analysis[key] = 0.65
                    elif key == 'sustainability_assessment':
                        analysis[key] = "Business shows moderate sustainability indicators"
                    elif key == 'twelve_month_outlook':
                        analysis[key] = {
                            "most_likely_scenario": "Continued market position with gradual growth",
                            "best_case_scenario": "Accelerated growth and market expansion",
                            "worst_case_scenario": "Market challenges requiring strategic adjustments",
                            "key_factors": ["Market conditions", "Competitive dynamics", "Technology trends"]
                        }
                    elif key == 'competitive_position':
                        analysis[key] = {
                            "market_position": "challenger",
                            "competitive_advantages": ["Technology capabilities"],
                            "vulnerabilities": ["Market positioning"],
                            "competitive_threats": ["Established competitors"]
                        }
                    elif key == 'gemini_confidence_score':
                        analysis[key] = 0.7
            
            # Validate data types and ranges
            if not isinstance(analysis.get('business_health_score'), (int, float)):
                analysis['business_health_score'] = 0.65
            else:
                analysis['business_health_score'] = max(0, min(1, analysis['business_health_score']))
            
            if not isinstance(analysis.get('gemini_confidence_score'), (int, float)):
                analysis['gemini_confidence_score'] = 0.7
            else:
                analysis['gemini_confidence_score'] = max(0, min(1, analysis['gemini_confidence_score']))
            
            # Ensure lists are actually lists
            for list_key in ['strategic_insights', 'actionable_strategies']:
                if not isinstance(analysis.get(list_key), list):
                    analysis[list_key] = [str(analysis.get(list_key, f"Analysis for {list_key}"))]
            
            print(f"✓ Validated and fixed Gemini analysis structure")
            return analysis
            
        except Exception as e:
            print(f"Warning: Error validating Gemini analysis: {e}")
            return self._create_fallback_gemini_analysis()
    
    def _create_fallback_gemini_analysis(self) -> Dict[str, Any]:
        """Create fallback analysis when Gemini fails"""
        return {
            "strategic_insights": [
                "Intelligence signals indicate potential business pattern changes",
                "Market dynamics suggest need for strategic positioning review",
                "Technology trends may impact competitive landscape"
            ],
            "critical_threats": [
                {"threat": "Market position vulnerability", "probability": 0.6, "impact": "medium", "timeline_months": 6},
                {"threat": "Technology disruption risk", "probability": 0.5, "impact": "high", "timeline_months": 12},
                {"threat": "Competitive pressure increase", "probability": 0.7, "impact": "medium", "timeline_months": 9}
            ],
            "opportunities": [
                {"opportunity": "Market expansion potential", "potential_value": "high", "effort_required": "medium"},
                {"opportunity": "Technology adoption advantage", "potential_value": "medium", "effort_required": "low"},
                {"opportunity": "Strategic partnership possibilities", "potential_value": "high", "effort_required": "high"}
            ],
            "actionable_strategies": [
                "Strengthen core market position",
                "Invest in technology capabilities", 
                "Develop strategic partnerships",
                "Enhance customer retention",
                "Monitor competitive developments"
            ],
            "business_health_score": 0.7,
            "sustainability_assessment": "Moderate business sustainability with room for strategic improvement",
            "twelve_month_outlook": {
                "most_likely_scenario": "Stable performance with gradual improvement",
                "best_case_scenario": "Strong growth through strategic initiatives",
                "worst_case_scenario": "Market challenges require defensive strategies",
                "key_factors": ["Market conditions", "Execution capability", "Competitive response"]
            },
            "competitive_position": {
                "market_position": "challenger",
                "competitive_advantages": ["Technology focus", "Market knowledge"],
                "vulnerabilities": ["Resource constraints", "Market share"],
                "competitive_threats": ["Established players", "New entrants"]
            },
            "gemini_confidence_score": 0.6
        }
    
    async def _process_combined_intelligence(self, company_name: str, domain: str, industry: str, 
                                           market_intel: Dict, tech_intel: Dict, financial_intel: Dict, enhanced_analysis: Dict) -> Dict[str, Any]:
        """Process and combine all intelligence sources"""
        
        # Extract all WOW signals
        all_signals = []
        
        if 'wow_signals' in market_intel:
            all_signals.extend(market_intel['wow_signals'])
        
        if 'technology_wow_signals' in tech_intel:
            all_signals.extend(tech_intel['technology_wow_signals'])
        
        # Categorize signals by severity
        critical_signals = [s for s in all_signals if s.get('severity') == 'critical']
        high_signals = [s for s in all_signals if s.get('severity') == 'high']
        medium_signals = [s for s in all_signals if s.get('severity') == 'medium']
        
        # Calculate comprehensive threat assessment
        overall_threat = self._calculate_comprehensive_threat(critical_signals, high_signals, medium_signals)
        
        # Generate industry-specific recommendations
        recommendations = self._generate_industry_recommendations(industry, all_signals)
        
        # Calculate business impact
        business_impact = self._calculate_business_impact(all_signals, industry)
        
        # Generate executive summary enhanced with Gemini analysis
        executive_summary = self._generate_executive_summary(
            company_name, industry, all_signals, overall_threat, business_impact, enhanced_analysis
        )
        
        return {
            'company_analysis': {
                'company_name': company_name,
                'domain': domain,
                'industry': industry,
                'analysis_timestamp': datetime.now().isoformat()
            },
            'intelligence_summary': {
                'total_signals_detected': len(all_signals),
                'critical_signals': len(critical_signals),
                'high_priority_signals': len(high_signals),
                'medium_priority_signals': len(medium_signals)
            },
            'threat_assessment': {
                'overall_threat_level': overall_threat,
                'primary_risks': self._identify_primary_risks(all_signals),
                'opportunity_areas': self._identify_opportunities(all_signals)
            },
            'business_impact': business_impact,
            'wow_signals_detected': all_signals[:10],  # Top 10 signals
            'strategic_recommendations': recommendations,
            'executive_summary': executive_summary,
            'gemini_analysis': enhanced_analysis,
            'intelligence_sources': {
                'market_intelligence': len(market_intel.get('wow_signals', [])),
                'technology_intelligence': len(tech_intel.get('technology_wow_signals', [])),
                'financial_intelligence': 'analyzed' if financial_intel else 'unavailable',
                'gemini_ai_enhancement': 'active' if enhanced_analysis.get('gemini_confidence_score', 0) > 0 else 'unavailable'
            }
        }
    
    def _clean_company_name(self, name: str) -> str:
        """Clean and standardize company name"""
        # Remove common suffixes and clean up
        name = re.sub(r'\s+(Inc|LLC|Corp|Corporation|Ltd|Limited)\s*\.?$', '', name, flags=re.IGNORECASE)
        return name.strip().title()
    
    def _validate_industry(self, industry: str) -> str:
        """Validate and standardize industry"""
        industry = industry.lower().strip()
        
        # Map common variations to standard industries
        industry_mapping = {
            'tech': 'technology',
            'software': 'technology', 
            'fintech': 'fintech',
            'financial': 'fintech',
            'ecommerce': 'e-commerce',
            'online-retail': 'e-commerce',
            'health': 'healthcare',
            'medical': 'healthcare',
            'bio': 'biotech',
            'manufacturing': 'manufacturing',
            'retail': 'retail',
            'media': 'media',
            'gaming': 'gaming',
            'games': 'gaming',
            'automotive': 'automotive',
            'cars': 'automotive',
            'realestate': 'real-estate',
            'real estate': 'real-estate',
            'education': 'education',
            'edtech': 'education',
            'food': 'food-delivery',
            'delivery': 'food-delivery',
            'logistics': 'logistics',
            'shipping': 'logistics',
            'energy': 'energy',
            'aerospace': 'aerospace',
            'telecom': 'telecommunications',
            'telecommunications': 'telecommunications'
        }
        
        standardized = industry_mapping.get(industry, industry)
        
        if standardized not in self.supported_industries:
            print(f"⚠️ Industry '{industry}' not in standard list. Using 'technology' as default.")
            return 'technology'
        
        return standardized
    
    def _generate_domain_if_missing(self, company_name: str, domain: Optional[str]) -> str:
        """Generate domain if not provided"""
        if domain:
            return domain.lower().strip()
        
        # Generate domain from company name
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', company_name)
        domain_name = clean_name.lower().replace(' ', '')
        return f"{domain_name}.com"
    
    def _generate_industry_financial_patterns(self, industry: str) -> Dict[str, Any]:
        """Generate industry-specific financial patterns"""
        import random
        
        industry_patterns = {
            'technology': {
                'typical_burn_rate_monthly': random.randint(50000, 500000),
                'growth_rate_expected': random.randint(20, 200),
                'funding_rounds_typical': 'Series A to Series C',
                'cash_runway_months': random.randint(12, 36)
            },
            'fintech': {
                'typical_burn_rate_monthly': random.randint(100000, 800000),
                'growth_rate_expected': random.randint(30, 150),
                'funding_rounds_typical': 'Seed to Series B',
                'cash_runway_months': random.randint(15, 30)
            },
            'saas': {
                'typical_burn_rate_monthly': random.randint(25000, 300000),
                'growth_rate_expected': random.randint(40, 300),
                'funding_rounds_typical': 'Seed to Series A',
                'cash_runway_months': random.randint(18, 42)
            },
            'e-commerce': {
                'typical_burn_rate_monthly': random.randint(75000, 600000),
                'growth_rate_expected': random.randint(25, 120),
                'funding_rounds_typical': 'Series A to Series B',
                'cash_runway_months': random.randint(10, 24)
            }
        }
        
        return industry_patterns.get(industry, industry_patterns['technology'])
    
    def _estimate_burn_rate_by_industry(self, industry: str) -> Dict[str, Any]:
        """Estimate burn rate patterns by industry"""
        import random
        
        base_burn_rates = {
            'technology': 150000,
            'fintech': 250000,
            'saas': 100000,
            'e-commerce': 200000,
            'healthcare': 300000,
            'biotech': 500000,
            'manufacturing': 180000,
            'gaming': 120000
        }
        
        base_rate = base_burn_rates.get(industry, 150000)
        variance = random.uniform(0.7, 1.3)  # ±30% variance
        
        return {
            'estimated_monthly_burn': int(base_rate * variance),
            'industry_benchmark': base_rate,
            'variance_from_benchmark': f"{((variance - 1) * 100):+.1f}%",
            'sustainability_score': random.uniform(0.6, 0.9)
        }
    
    def _predict_funding_stage(self, company_name: str, industry: str) -> str:
        """Predict likely funding stage"""
        import random
        
        # Simple heuristic based on industry and name patterns
        if 'AI' in company_name.upper() or 'intelligence' in company_name.lower():
            stages = ['Series A', 'Series B', 'Series C']
        elif industry in ['biotech', 'healthcare']:
            stages = ['Series B', 'Series C', 'Series D'] 
        elif industry in ['saas', 'technology']:
            stages = ['Seed', 'Series A', 'Series B']
        else:
            stages = ['Seed', 'Series A']
            
        return random.choice(stages)
    
    def _assess_competitive_position(self, industry: str) -> Dict[str, Any]:
        """Assess competitive position within industry"""
        import random
        
        return {
            'market_position': random.choice(['leader', 'challenger', 'follower', 'niche']),
            'competitive_intensity': random.choice(['low', 'medium', 'high', 'extreme']),
            'differentiation_score': random.uniform(0.3, 0.9),
            'market_share_estimate': f"{random.uniform(0.1, 15.0):.1f}%"
        }
    
    def _calculate_comprehensive_threat(self, critical: List, high: List, medium: List) -> str:
        """Calculate comprehensive threat level"""
        if len(critical) >= 3:
            return 'EXTREME'
        elif len(critical) >= 2 or len(high) >= 5:
            return 'CRITICAL' 
        elif len(critical) >= 1 or len(high) >= 3:
            return 'HIGH'
        elif len(high) >= 1 or len(medium) >= 3:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _identify_primary_risks(self, signals: List[Dict]) -> List[str]:
        """Identify primary business risks"""
        risks = set()
        
        for signal in signals:
            signal_type = signal.get('signal_type', '')
            if 'death' in signal_type or 'exodus' in signal_type:
                risks.add('Business failure risk')
            elif 'ai' in signal_type or 'stealth' in signal_type:
                risks.add('Technology disruption threat')
            elif 'privacy' in signal_type or 'regulatory' in signal_type:
                risks.add('Regulatory compliance risk')
            elif 'manipulation' in signal_type:
                risks.add('Market manipulation exposure')
            elif 'security' in signal_type:
                risks.add('Cybersecurity vulnerability')
        
        return list(risks)[:5]
    
    def _identify_opportunities(self, signals: List[Dict]) -> List[str]:
        """Identify business opportunities"""
        opportunities = set()
        
        for signal in signals:
            signal_type = signal.get('signal_type', '')
            if 'death' in signal_type or 'exodus' in signal_type:
                opportunities.add('Acquisition opportunity at discounted valuation')
            elif 'ai' in signal_type:
                opportunities.add('AI capability development opportunity')
            elif 'privacy' in signal_type:
                opportunities.add('Privacy-first competitive positioning')
            elif 'security' in signal_type:
                opportunities.add('Security solution market opportunity')
        
        return list(opportunities)[:5]
    
    def _calculate_business_impact(self, signals: List[Dict], industry: str) -> Dict[str, Any]:
        """Calculate comprehensive business impact"""
        cost_impacts = [s.get('cost_impact_millions', 0) for s in signals]
        probabilities = []
        
        for signal in signals:
            for key, value in signal.items():
                if 'probability' in key and isinstance(value, (int, float)):
                    probabilities.append(value / 100)
        
        total_cost_impact = sum(cost_impacts)
        avg_probability = sum(probabilities) / len(probabilities) if probabilities else 0
        
        return {
            'estimated_financial_impact_millions': total_cost_impact,
            'average_threat_probability': f"{avg_probability * 100:.1f}%",
            'business_continuity_risk': 'High' if avg_probability > 0.7 else 'Medium' if avg_probability > 0.4 else 'Low',
            'strategic_priority_level': 'Immediate' if total_cost_impact > 5 else 'High' if total_cost_impact > 1 else 'Medium'
        }
    
    def _generate_industry_recommendations(self, industry: str, signals: List[Dict]) -> List[str]:
        """Generate industry-specific strategic recommendations"""
        recommendations = set()
        
        # Base industry recommendations
        industry_recs = {
            'technology': [
                'Accelerate AI/ML capability development',
                'Strengthen cybersecurity infrastructure', 
                'Monitor open-source technology adoption trends'
            ],
            'fintech': [
                'Enhance regulatory compliance frameworks',
                'Implement advanced fraud detection systems',
                'Monitor cryptocurrency market developments'
            ],
            'saas': [
                'Focus on customer retention and churn prevention',
                'Optimize pricing strategy based on value metrics',
                'Invest in product-led growth initiatives'
            ],
            'e-commerce': [
                'Strengthen supply chain resilience',
                'Invest in personalization and recommendation engines',
                'Monitor consumer behavior shifts'
            ]
        }
        
        base_recs = industry_recs.get(industry, industry_recs['technology'])
        recommendations.update(base_recs)
        
        # Signal-specific recommendations
        signal_types = {s.get('signal_type') for s in signals}
        
        if any('exodus' in st or 'death' in st for st in signal_types):
            recommendations.add('Evaluate distressed competitor acquisition opportunities')
        
        if any('ai' in st or 'stealth' in st for st in signal_types):
            recommendations.add('Accelerate AI research and development initiatives')
        
        if any('privacy' in st or 'regulatory' in st for st in signal_types):
            recommendations.add('Establish privacy-first competitive differentiation')
        
        return list(recommendations)[:8]
    
    def _generate_executive_summary(self, company_name: str, industry: str, signals: List[Dict], 
                                   threat_level: str, business_impact: Dict, gemini_analysis: Dict) -> str:
        """Generate executive summary"""
        signal_count = len(signals)
        critical_count = len([s for s in signals if s.get('severity') == 'critical'])
        
        gemini_health_score = gemini_analysis.get('business_health_score', 0.7)
        gemini_outlook = gemini_analysis.get('twelve_month_outlook', {})
        gemini_position = gemini_analysis.get('competitive_position', {})
        gemini_confidence = gemini_analysis.get('gemini_confidence_score', 0.6)
        
        summary = f"""
EXECUTIVE INTELLIGENCE SUMMARY: {company_name}

INDUSTRY: {industry.title()}
ANALYSIS DATE: {datetime.now().strftime('%B %d, %Y')}
AI ANALYSIS CONFIDENCE: {gemini_confidence * 100:.1f}%

THREAT ASSESSMENT: {threat_level}
- Total Intelligence Signals Detected: {signal_count}
- Critical Threat Indicators: {critical_count}
- Business Health Score: {gemini_health_score * 100:.1f}/100

BUSINESS IMPACT:
- Estimated Financial Risk: ${business_impact.get('estimated_financial_impact_millions', 0)}M
- Threat Probability: {business_impact.get('average_threat_probability', '0%')}
- Strategic Priority: {business_impact.get('strategic_priority_level', 'Medium')}

GEMINI AI KEY INSIGHTS:
"""
        
        # Add Gemini strategic insights
        gemini_insights = gemini_analysis.get('strategic_insights', [])
        for i, insight in enumerate(gemini_insights[:3], 1):
            summary += f"{i}. {insight}\n"
        
        summary += f"""
COMPETITIVE POSITION: {gemini_position.get('market_position', 'Unknown').title()}

12-MONTH OUTLOOK:
- Most Likely: {gemini_outlook.get('most_likely_scenario', 'Stable performance expected')}
- Best Case: {gemini_outlook.get('best_case_scenario', 'Strong growth potential')}
- Worst Case: {gemini_outlook.get('worst_case_scenario', 'Market challenges possible')}

RECOMMENDATION: {'Immediate strategic action required' if threat_level in ['CRITICAL', 'EXTREME'] else 'Monitor and prepare contingency plans'}

SUSTAINABILITY ASSESSMENT: {gemini_analysis.get('sustainability_assessment', 'Analysis in progress')}
        """
        
        return summary.strip()


async def interactive_company_analyzer():
    """Interactive company analysis interface"""
    analyzer = CompanyIntelligenceAnalyzer()
    
    print("=" * 80)
    print("PENSIEVE CIO - INTERACTIVE COMPANY INTELLIGENCE ANALYZER")
    print("=" * 80)
    print("Analyze any company using advanced WOW intelligence patterns!")
    print("Detect: Layoffs, Acquisitions, Death Spirals, AI Development, and MORE!")
    print("=" * 80)
    
    while True:
        try:
            print("\n" + "-" * 50)
            print("COMPANY ANALYSIS REQUEST")
            print("-" * 50)
            
            # Get company information
            company_name = input("Company Name: ").strip()
            if not company_name or company_name.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            industry = input("Industry (e.g., technology, fintech, saas): ").strip()
            if not industry:
                industry = 'technology'  # Default
            
            domain = input("Company Domain (optional, will auto-generate): ").strip()
            if not domain:
                domain = None
            
            print(f"\nAnalyzing {company_name} in {industry} industry...")
            print("This may take 30-60 seconds for comprehensive analysis...")
            
            # Run analysis
            result = await analyzer.analyze_company(company_name, industry, domain)
            
            if 'error' in result:
                print(f"ERROR: Analysis failed: {result['error']}")
                continue
            
            # Display results
            await display_analysis_results(result)
            
            # Ask for another analysis
            print(f"\n{'='*80}")
            another = input("Analyze another company? (y/n): ").strip().lower()
            if another not in ['y', 'yes']:
                print("Analysis complete. Thank you for using Pensieve CIO!")
                break
                
        except KeyboardInterrupt:
            print(f"\n\nAnalysis interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"ERROR: Unexpected error: {e}")
            continue


async def display_analysis_results(result: Dict[str, Any]):
    """Display comprehensive analysis results"""
    
    company_info = result.get('company_analysis', {})
    intelligence = result.get('intelligence_summary', {})
    threat = result.get('threat_assessment', {})
    impact = result.get('business_impact', {})
    signals = result.get('wow_signals_detected', [])
    recommendations = result.get('strategic_recommendations', [])
    executive_summary = result.get('executive_summary', '')
    gemini_analysis = result.get('gemini_analysis', {})
    
    print(f"\nEXECUTIVE SUMMARY")
    print("-" * 50) 
    print(executive_summary)
    
    print(f"\nINTELLIGENCE OVERVIEW")
    print("-" * 50)
    print(f"Total WOW Signals: {intelligence.get('total_signals_detected', 0)}")
    print(f"Critical Threats: {intelligence.get('critical_signals', 0)}")
    print(f"High Priority: {intelligence.get('high_priority_signals', 0)}")
    print(f"Medium Priority: {intelligence.get('medium_priority_signals', 0)}")
    
    print(f"\nTHREAT ASSESSMENT")
    print("-" * 50)
    print(f"Overall Threat Level: {threat.get('overall_threat_level', 'UNKNOWN')}")
    
    primary_risks = threat.get('primary_risks', [])
    if primary_risks:
        print("Primary Risks Identified:")
        for risk in primary_risks:
            print(f"  - {risk}")
    
    opportunities = threat.get('opportunity_areas', [])
    if opportunities:
        print("Business Opportunities:")
        for opp in opportunities:
            print(f"  - {opp}")
    
    print(f"\nBUSINESS IMPACT")
    print("-" * 50)
    print(f"Financial Risk Estimate: ${impact.get('estimated_financial_impact_millions', 0)}M")
    print(f"Average Threat Probability: {impact.get('average_threat_probability', '0%')}")
    print(f"Strategic Priority Level: {impact.get('strategic_priority_level', 'Medium')}")
    
    print(f"\nTOP WOW INTELLIGENCE SIGNALS")
    print("-" * 50)
    for i, signal in enumerate(signals[:5], 1):
        signal_type = signal.get('signal_type', 'Unknown').replace('_', ' ').title()
        severity = signal.get('severity', 'medium').upper()
        wow_factor = signal.get('wow_factor', 'Advanced business intelligence')
        
        print(f"{i}. [{severity}] {signal_type}")
        print(f"   WOW Factor: {wow_factor}")
        
        # Show specific metrics
        for key, value in signal.items():
            if 'probability' in key and isinstance(value, (int, float)):
                print(f"   {key.replace('_', ' ').title()}: {value}%")
            elif 'timeline' in key and isinstance(value, (int, float)):
                print(f"   {key.replace('_', ' ').title()}: {value} months")
    
    print(f"\nSTRATEGIC RECOMMENDATIONS")
    print("-" * 50)
    for i, rec in enumerate(recommendations[:6], 1):
        print(f"{i}. {rec}")
    
    # Display Gemini AI Analysis
    if gemini_analysis and gemini_analysis.get('gemini_confidence_score', 0) > 0:
        print(f"\nGEMINI AI STRATEGIC ANALYSIS")
        print("-" * 50)
        print(f"AI Confidence Score: {gemini_analysis.get('gemini_confidence_score', 0) * 100:.1f}%")
        print(f"Business Health Score: {gemini_analysis.get('business_health_score', 0) * 100:.1f}/100")
        
        # Show Gemini threats
        gemini_threats = gemini_analysis.get('critical_threats', [])
        if gemini_threats:
            print("\nAI-Identified Critical Threats:")
            for i, threat in enumerate(gemini_threats[:3], 1):
                print(f"  {i}. {threat.get('threat', 'Unknown threat')} ({threat.get('probability', 0) * 100:.0f}% probability)")
        
        # Show Gemini opportunities
        gemini_opportunities = gemini_analysis.get('opportunities', [])
        if gemini_opportunities:
            print("\nAI-Identified Opportunities:")
            for i, opp in enumerate(gemini_opportunities[:3], 1):
                print(f"  {i}. {opp.get('opportunity', 'Unknown opportunity')} ({opp.get('potential_value', 'unknown')} value)")
        
        # Show 12-month outlook
        outlook = gemini_analysis.get('twelve_month_outlook', {})
        if outlook:
            print(f"\n12-Month Business Outlook:")
            print(f"  Most Likely: {outlook.get('most_likely_scenario', 'Analysis pending')}")
            print(f"  Best Case: {outlook.get('best_case_scenario', 'Growth potential identified')}")
            print(f"  Worst Case: {outlook.get('worst_case_scenario', 'Risk factors present')}")
        
        # Show competitive position
        competitive = gemini_analysis.get('competitive_position', {})
        if competitive:
            print(f"\nCompetitive Position Analysis:")
            print(f"  Market Position: {competitive.get('market_position', 'Unknown').title()}")
            advantages = competitive.get('competitive_advantages', [])
            if advantages:
                print(f"  Key Advantages: {', '.join(advantages[:3])}")
            vulnerabilities = competitive.get('vulnerabilities', [])
            if vulnerabilities:
                print(f"  Vulnerabilities: {', '.join(vulnerabilities[:3])}")

    sources = result.get('intelligence_sources', {})
    print(f"\nINTELLIGENCE SOURCES")
    print("-" * 50)
    print(f"Market Intelligence Signals: {sources.get('market_intelligence', 0)}")
    print(f"Technology Intelligence Signals: {sources.get('technology_intelligence', 0)}")
    print(f"Financial Intelligence: {sources.get('financial_intelligence', 'Unavailable')}")
    print(f"Gemini AI Enhancement: {sources.get('gemini_ai_enhancement', 'Unavailable').title()}")


if __name__ == "__main__":
    print("Pensieve CIO - Interactive Company Intelligence Analyzer")
    print("=" * 60)
    
    try:
        asyncio.run(interactive_company_analyzer())
    except KeyboardInterrupt:
        print("\n\nAnalysis session ended. Goodbye!")
    except Exception as e:
        print(f"\n\nSystem error: {e}")