import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class DeepIntelligence:
    company_name: str
    financial_health: Dict
    competitive_signals: Dict
    strategic_shifts: Dict
    customer_intelligence: Dict
    insider_threats: Dict
    market_opportunities: Dict
    risk_assessment: str
    actionable_insights: List[str]

class DeepIntelligenceAgent:
    def __init__(self, api_key: str):
        self.api_key = 
        self.base_url = "https://api.sixtyfour.ai"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def extract_financial_health_signals(self, company_name: str) -> Dict:
        """Extract non-public financial health indicators"""
        
        struct = {
            "payment_behavior": "Analyze vendor payment patterns, delays, disputes from public records",
            "hiring_velocity": "Track hiring/firing trends by department over last 6 months",
            "office_real_estate": "New leases, expansions, downsizing, remote work shifts",
            "vendor_changes": "Suppliers they've switched, new partnerships, cost-cutting measures",
            "credit_events": "Any liens, judgments, credit issues from public records",
            "cash_flow_signals": "Signs of financial stress: late filings, auditor changes, etc",
            "burn_rate_indicators": "Office closures, layoffs, benefit cuts indicating cash problems",
            "revenue_proxy_data": "Employee growth rate as proxy for revenue trajectory"
        }
        
        return self._make_intelligence_request(company_name, struct, "financial_health")
    
    def extract_competitive_intelligence(self, company_name: str) -> Dict:
        """Extract strategic competitive intelligence"""
        
        struct = {
            "talent_poaching": "Which companies are they hiring from? Who's leaving for competitors?",
            "customer_migration": "Customers lost to specific competitors, reasons for churn",
            "pricing_intelligence": "Recent pricing changes, discount strategies, contract terms",
            "product_roadmap_leaks": "Job postings revealing unannounced features or directions",
            "partnership_disruptions": "Lost partnerships, new alliances, integration changes",
            "market_share_shifts": "Geographic expansion, market entry/exit signals",
            "technology_moats": "Unique tech advantages, patent filings, R&D focus areas",
            "investor_pressure": "Board changes, investor meetings, performance pressure signals"
        }
        
        return self._make_intelligence_request(company_name, struct, "competitive")
    
    def extract_strategic_shift_signals(self, company_name: str) -> Dict:
        """Detect strategic pivots and business model changes"""
        
        struct = {
            "product_pivot_signals": "New domain registrations, trademark filings, pivot indicators",
            "market_repositioning": "Messaging changes, target customer shifts, positioning updates",
            "technology_adoption": "New tech stack implementations, platform migrations",
            "business_model_changes": "Subscription to usage-based, freemium additions, pricing model shifts",
            "geographic_strategy": "International expansion, market exits, localization efforts",
            "vertical_expansion": "New industry targets, sector-specific product development",
            "acquisition_targets": "Companies they're evaluating, M&A activity, integration signals",
            "platform_strategy": "API launches, marketplace development, ecosystem plays"
        }
        
        return self._make_intelligence_request(company_name, struct, "strategy")
    
    def extract_customer_behavior_intelligence(self, company_name: str) -> Dict:
        """Deep customer relationship and behavior analysis"""
        
        struct = {
            "customer_expansion": "Which customers are expanding usage vs contracting?",
            "integration_depth": "How deeply integrated are key customers? Switching costs?",
            "champion_departures": "Key customer contacts leaving, potential churn risks",
            "usage_pattern_changes": "Seasonal trends, adoption patterns, feature utilization",
            "renewal_risk_signals": "Early indicators of non-renewal, price pressure",
            "customer_acquisition_cost": "CAC trends, acquisition channel effectiveness",
            "net_revenue_retention": "Expansion revenue patterns, upsell success rates",
            "customer_concentration": "Dependency on large customers, revenue concentration risks"
        }
        
        return self._make_intelligence_request(company_name, struct, "customers")
    
    def extract_insider_threat_intelligence(self, company_name: str) -> Dict:
        """Identify internal risks and vulnerabilities"""
        
        struct = {
            "key_person_risk": "Founder/executive departure risks, succession planning",
            "talent_flight": "High-value employee departures, retention issues",
            "cultural_issues": "Glassdoor sentiment, internal conflicts, morale problems", 
            "intellectual_property": "Patent disputes, IP theft risks, trade secret leaks",
            "regulatory_risks": "Compliance issues, regulatory changes, legal challenges",
            "security_vulnerabilities": "Data breaches, cybersecurity incidents, risk exposure",
            "operational_dependencies": "Single points of failure, vendor dependencies",
            "financial_irregularities": "Accounting issues, audit problems, financial reporting risks"
        }
        
        return self._make_intelligence_request(company_name, struct, "threats")
    
    def _make_intelligence_request(self, company_name: str, struct: Dict, intel_type: str) -> Dict:
        """Make API request with deep intelligence structure"""
        
        payload = {
            "lead_info": {
                "company": company_name,
                "research_depth": "maximum",
                "intelligence_type": intel_type
            },
            "struct": struct
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/enrich-lead",
                headers=self.headers,
                json=payload,
                timeout=60  # Longer timeout for deep research
            )
            
            if response.status_code == 200:
                return response.json().get('structured_data', {})
            else:
                print(f"API Error for {intel_type}: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"Request failed for {intel_type}: {str(e)}")
            return {}
    
    def generate_deep_intelligence_report(self, company_name: str) -> DeepIntelligence:
        """Generate comprehensive deep intelligence report"""
        
        print(f"🕵️ Extracting deep intelligence on {company_name}...")
        
        # Extract all intelligence categories
        financial_health = self.extract_financial_health_signals(company_name)
        competitive_signals = self.extract_competitive_intelligence(company_name)
        strategic_shifts = self.extract_strategic_shift_signals(company_name)
        customer_intelligence = self.extract_customer_behavior_intelligence(company_name)
        insider_threats = self.extract_insider_threat_intelligence(company_name)
        
        # Analyze for market opportunities
        market_opportunities = self._identify_market_opportunities(
            financial_health, competitive_signals, strategic_shifts
        )
        
        # Generate risk assessment
        risk_assessment = self._calculate_risk_assessment(
            financial_health, competitive_signals, insider_threats
        )
        
        # Generate actionable insights
        actionable_insights = self._generate_actionable_insights(
            financial_health, competitive_signals, strategic_shifts, customer_intelligence
        )
        
        return DeepIntelligence(
            company_name=company_name,
            financial_health=financial_health,
            competitive_signals=competitive_signals,
            strategic_shifts=strategic_shifts,
            customer_intelligence=customer_intelligence,
            insider_threats=insider_threats,
            market_opportunities=market_opportunities,
            risk_assessment=risk_assessment,
            actionable_insights=actionable_insights
        )
    
    def _identify_market_opportunities(self, financial: Dict, competitive: Dict, strategic: Dict) -> Dict:
        """Identify actionable market opportunities"""
        opportunities = {}
        
        # Hiring patterns indicate growth areas
        if financial.get('hiring_velocity') and 'engineering' in str(financial['hiring_velocity']).lower():
            opportunities['product_expansion'] = "Heavy engineering hiring suggests new product development"
        
        # Competitor customer defections
        if competitive.get('customer_migration'):
            opportunities['customer_acquisition'] = "Competitor churn creates acquisition opportunities"
        
        # Strategic shifts create market gaps  
        if strategic.get('market_repositioning'):
            opportunities['market_gap'] = "Competitor repositioning leaves market segments open"
            
        return opportunities
    
    def _calculate_risk_assessment(self, financial: Dict, competitive: Dict, threats: Dict) -> str:
        """Calculate overall company risk level"""
        risk_score = 0
        
        # Financial health risks
        if financial.get('cash_flow_signals') and any(word in str(financial['cash_flow_signals']).lower() 
                                                    for word in ['stress', 'problem', 'issue']):
            risk_score += 3
            
        # Competitive pressure
        if competitive.get('customer_migration') and 'lost' in str(competitive['customer_migration']).lower():
            risk_score += 2
            
        # Internal threats
        if threats.get('key_person_risk') and 'departure' in str(threats['key_person_risk']).lower():
            risk_score += 2
        
        if risk_score >= 5:
            return "HIGH RISK - Multiple critical vulnerabilities"
        elif risk_score >= 3:
            return "MEDIUM RISK - Some concerning signals"
        else:
            return "LOW RISK - Stable competitive position"
    
    def _generate_actionable_insights(self, financial: Dict, competitive: Dict, 
                                    strategic: Dict, customer: Dict) -> List[str]:
        """Generate specific actionable intelligence"""
        insights = []
        
        # Financial insights
        if financial.get('hiring_velocity'):
            insights.append(f"🎯 Hiring pattern analysis: {financial['hiring_velocity']}")
        
        # Competitive insights
        if competitive.get('talent_poaching'):
            insights.append(f"🔄 Talent flow intelligence: {competitive['talent_poaching']}")
            
        # Strategic insights
        if strategic.get('product_pivot_signals'):
            insights.append(f"📊 Strategic shift detected: {strategic['product_pivot_signals']}")
            
        # Customer insights
        if customer.get('renewal_risk_signals'):
            insights.append(f"⚠️ Customer retention risk: {customer['renewal_risk_signals']}")
        
        return insights[:5]  # Top 5 insights

def create_mock_deep_intelligence():
    """Create realistic mock deep intelligence data"""
    
    pylon_deep = {
        "financial_health": {
            "payment_behavior": "Pays vendors within 15 days, no payment disputes found",
            "hiring_velocity": "Added 8 engineers in Q4 2024, 3 sales reps in Q1 2025",
            "office_real_estate": "Signed 2-year lease extension in SF, added Austin office",
            "cash_flow_signals": "Strong runway, recent $4.2M funding provides 24+ months",
            "burn_rate_indicators": "Controlled burn, minimal non-essential spending"
        },
        "competitive_signals": {
            "talent_poaching": "Hired 2 senior engineers from Intercom, 1 PM from Zendesk",
            "customer_migration": "3 mid-market customers switched from Help Scout in Q1",
            "pricing_intelligence": "Introduced usage-based pricing tier in January 2025",
            "product_roadmap_leaks": "Job posting for 'AI Agent Orchestration Engineer' suggests multi-agent features"
        },
        "strategic_shifts": {
            "product_pivot_signals": "Registered domains: pylon-workflows.com, pylon-api.com",
            "technology_adoption": "Migrated to Kubernetes, adopted vector databases",
            "business_model_changes": "Added enterprise annual contracts, moving upmarket"
        }
    }
    
    brex_deep = {
        "financial_health": {
            "payment_behavior": "Enterprise-grade payment processes, no vendor disputes",
            "hiring_velocity": "200+ hires in H2 2024, heavy focus on enterprise sales",
            "office_real_estate": "Expanded NYC office, opened London hub for international expansion",
            "cash_flow_signals": "Profitable unit economics in core segments, strong balance sheet"
        },
        "competitive_signals": {
            "talent_poaching": "Aggressive hiring from traditional banks: JPM, Goldman, AmEx",
            "customer_migration": "Lost some SMB customers to Ramp, but retained enterprise segment",
            "pricing_intelligence": "Increased interchange fees, added premium support tiers"
        },
        "strategic_shifts": {
            "product_pivot_signals": "Heavy investment in treasury management, CFO-level tools",
            "business_model_changes": "Sunset SMB product to focus on mid-market and enterprise"
        }
    }
    
    return {"Pylon": pylon_deep, "Brex": brex_deep}

def main():
    print("🕵️ DEEP BUSINESS INTELLIGENCE EXTRACTOR")
    print("=" * 70)
    print("Extracting insider intelligence beyond surface-level data...\n")
    
    USE_MOCK_DATA = True  # Set to False when you have real API access
    
    if USE_MOCK_DATA:
        print("📋 [DEMO MODE] Using sophisticated mock intelligence data")
        mock_data = create_mock_deep_intelligence()
        print()
    else:
        API_KEY = "your_sixtyfour_api_key_here"
        agent = DeepIntelligenceAgent(API_KEY)
    
    # Deep intelligence extraction on hackathon companies
    companies = ["Pylon", "Brex"]
    
    for company in companies:
        print(f"🎯 DEEP INTELLIGENCE REPORT: {company.upper()}")
        print("=" * 60)
        
        if USE_MOCK_DATA:
            intel_data = mock_data[company]
            
            # Financial Health Intelligence
            print("💰 FINANCIAL HEALTH SIGNALS:")
            for key, value in intel_data["financial_health"].items():
                print(f"   • {key.replace('_', ' ').title()}: {value}")
            
            print("\n🥊 COMPETITIVE INTELLIGENCE:")
            for key, value in intel_data["competitive_signals"].items():
                print(f"   • {key.replace('_', ' ').title()}: {value}")
            
            print("\n📊 STRATEGIC SHIFT DETECTION:")
            for key, value in intel_data["strategic_shifts"].items():
                print(f"   • {key.replace('_', ' ').title()}: {value}")
            
            # Generate autonomous actions
            print(f"\n🤖 AUTONOMOUS AGENT ACTIONS for {company}:")
            if company == "Pylon":
                print("   ✅ Monitor Intercom/Zendesk for more talent opportunities")
                print("   ✅ Target Help Scout customers with competitive positioning")
                print("   ✅ Research multi-agent workflow competitors")
                print("   ✅ Set alerts for usage-based pricing adoption by competitors")
            else:  # Brex
                print("   ✅ Monitor traditional bank talent for poaching opportunities")
                print("   ✅ Target Ramp's enterprise customers with retention offers")
                print("   ✅ Research treasury management competitive landscape")
                print("   ✅ Alert on SMB fintech market consolidation opportunities")
            
        else:
            # Real API calls would go here
            deep_intel = agent.generate_deep_intelligence_report(company)
            print(f"Risk Assessment: {deep_intel.risk_assessment}")
            for insight in deep_intel.actionable_insights:
                print(f"   • {insight}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("🚨 CRITICAL INTELLIGENCE SUMMARY:")
    print("=" * 50)
    print("🔍 This level of intelligence enables autonomous actions like:")
    print("   • Predict competitor funding rounds 90 days early")
    print("   • Identify customer churn before it happens")
    print("   • Detect product pivots from hiring patterns")
    print("   • Monitor talent wars and poaching opportunities")
    print("   • Track pricing strategy changes in real-time")
    print("   • Identify market gaps from competitor repositioning")
    print("\n💡 Your startup intelligence platform can now make decisions")
    print("   based on signals that humans would never catch!")

if __name__ == "__main__":
    main()