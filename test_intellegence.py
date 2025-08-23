import requests
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class CompanyIntel:
    name: str
    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    industry: str
    tech_stack: List[str]
    employee_count: Optional[str]
    revenue_estimate: Optional[str]
    funding_status: Optional[str]
    key_contacts: List[str]
    competitive_threats: List[str]
    notes: str

class SixtyfourClient:
    def __init__(self, api_key: str):
        self.api_key = api_yj9TfC1UL5MFUpVmjjpb4rCtErtoPaYk
        self.base_url = "https://api.sixtyfour.ai"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def enrich_company(self, company_name: str, contact_info: Dict = None) -> CompanyIntel:
        """Fetch deep intelligence on a company"""
        
        lead_info = {
            "company": company_name
        }
        
        if contact_info:
            lead_info.update(contact_info)
            
        payload = {
            "lead_info": lead_info,
            "struct": {
                "name": "Company full legal name",
                "email": "Primary business email address", 
                "phone": "Main business phone number",
                "website": "Primary company website URL",
                "industry": "Primary industry and business vertical",
                "tech_stack": "List all technologies, tools, and platforms they use",
                "employee_count": "Estimated number of employees",
                "revenue_estimate": "Estimated annual revenue",
                "funding_status": "Recent funding rounds, investors, valuation",
                "key_contacts": "List of decision makers with titles and contact info",
                "competitive_landscape": "Main competitors and market position",
                "recent_news": "Recent company news, launches, or changes",
                "growth_signals": "Signs of expansion, hiring, or market changes"
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/enrich-lead",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_company_data(data)
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None
    
    def _parse_company_data(self, raw_data: Dict) -> CompanyIntel:
        """Parse API response into CompanyIntel object"""
        structured = raw_data.get('structured_data', {})
        notes = raw_data.get('notes', '')
        
        return CompanyIntel(
            name=structured.get('name', ''),
            email=structured.get('email'),
            phone=structured.get('phone'),
            website=structured.get('website'),
            industry=structured.get('industry', ''),
            tech_stack=self._parse_tech_stack(structured.get('tech_stack', '')),
            employee_count=structured.get('employee_count'),
            revenue_estimate=structured.get('revenue_estimate'),
            funding_status=structured.get('funding_status'),
            key_contacts=self._parse_contacts(structured.get('key_contacts', '')),
            competitive_threats=self._parse_competitors(structured.get('competitive_landscape', '')),
            notes=notes
        )
    
    def _parse_tech_stack(self, tech_string: str) -> List[str]:
        """Parse technology stack from string"""
        if not tech_string:
            return []
        # Simple parsing - you might want more sophisticated logic
        return [tech.strip() for tech in tech_string.split(',') if tech.strip()]
    
    def _parse_contacts(self, contacts_string: str) -> List[str]:
        """Parse key contacts from string"""
        if not contacts_string:
            return []
        return [contact.strip() for contact in contacts_string.split('\n') if contact.strip()]
    
    def _parse_competitors(self, competitors_string: str) -> List[str]:
        """Parse competitors from string"""
        if not competitors_string:
            return []
        return [comp.strip() for comp in competitors_string.split(',') if comp.strip()]

def fetch_competitive_intelligence(client: SixtyfourClient, competitors: List[str]) -> Dict:
    """Fetch intelligence on multiple competitors"""
    intel_report = {}
    
    for competitor in competitors:
        print(f"🔍 Researching {competitor}...")
        intel = client.enrich_company(competitor)
        
        if intel:
            intel_report[competitor] = {
                "threat_level": calculate_threat_level(intel),
                "tech_overlap": intel.tech_stack,
                "funding_status": intel.funding_status,
                "employee_growth": intel.employee_count,
                "key_intel": intel.notes[:200] + "..." if len(intel.notes) > 200 else intel.notes
            }
            
        # Rate limiting - be nice to the API
        time.sleep(1)
    
    return intel_report

def calculate_threat_level(intel: CompanyIntel) -> str:
    """Simple threat assessment based on company data"""
    threat_score = 0
    
    # Check funding status
    if intel.funding_status and any(word in intel.funding_status.lower() for word in ['series', 'funding', 'million']):
        threat_score += 2
    
    # Check employee count
    if intel.employee_count and any(word in intel.employee_count.lower() for word in ['100+', 'growing', 'hiring']):
        threat_score += 1
        
    # Check recent activity
    if 'expansion' in intel.notes.lower() or 'launch' in intel.notes.lower():
        threat_score += 1
    
    if threat_score >= 3:
        return "HIGH"
    elif threat_score >= 2:
        return "MEDIUM" 
    else:
        return "LOW"

def create_mock_data():
    """Create realistic mock data for demo purposes"""
    
    pylon_intel = CompanyIntel(
        name="Pylon AI",
        email="team@pylon.com", 
        phone="(555) 123-4567",
        website="https://pylon.com",
        industry="B2B SaaS, Customer Support AI",
        tech_stack=["React", "Node.js", "Python", "PostgreSQL", "AWS", "OpenAI API", "Stripe", "Intercom"],
        employee_count="15-25 employees", 
        revenue_estimate="$2-5M ARR",
        funding_status="Y Combinator W23, $4.2M seed round led by Bessemer Venture Partners",
        key_contacts=[
            "Marty Kausas - Co-founder & CEO (marty@pylon.com)",
            "Advith Chelikani - Co-founder & CTO (advith@pylon.com)", 
            "Robert Eng - Co-founder & VP Engineering (robert@pylon.com)"
        ],
        competitive_threats=["Zendesk", "Intercom", "Help Scout", "Ada", "Freshworks"],
        notes="Pylon (YC W23) is an AI-native B2B support system automating repetitive support work. Founded by Marty Kausas, Advith Chelikani, and Robert Eng. Unlike B2C support tools focusing on ticket deflection, Pylon handles complex B2B support prework and surfaces rich account context including churn risk and security sensitivity. Rapidly growing with enterprise customers, strong product-market fit in mid-market B2B companies. Recent expansion into automated workflow orchestration and deep CRM integrations."
    )
    
    brex_intel = CompanyIntel(
        name="Brex Inc.",
        email="contact@brex.com",
        phone="(855) 739-6739", 
        website="https://brex.com",
        industry="Fintech, Corporate Banking, Expense Management",
        tech_stack=["React", "Scala", "Python", "Kubernetes", "AWS", "PostgreSQL", "Kafka", "Snowflake"],
        employee_count="1,000+ employees",
        revenue_estimate="$200M+ ARR", 
        funding_status="Series D, $1.2B valuation, backed by Andreessen Horowitz, Y Combinator W17",
        key_contacts=[
            "Pedro Franceschi - Co-founder & CEO (pedro@brex.com)",
            "Henrique Dubugras - Co-founder & Co-CEO (henrique@brex.com)",
            "Michael Tannenbaum - CFO (michael.t@brex.com)"
        ],
        competitive_threats=["Ramp", "Mercury", "Stripe Corporate Card", "American Express", "JPMorgan Chase"],
        notes="Brex (YC W17) provides financial stack for startups from incorporation to IPO. Manages company spending, vendor payments, credit cards, bill pay, and reimbursements. Serves 1 in 3 venture-backed US startups with 20x higher credit limits than traditional banks. Strong moat in startup banking with sophisticated underwriting models. Recent pivot to focus on larger companies after shuttering SMB product. Expanding internationally and adding more banking services."
    )
    
    return {
        "Pylon": pylon_intel,
        "Brex": brex_intel
    }

def main():
    print("🎯 SIXTYFOUR API INTELLIGENCE DEMO")
    print("=" * 60)
    print("Testing with hackathon sponsor companies...\n")
    
    # Use mock data for demo (replace with real API calls when you have keys)
    USE_MOCK_DATA = True  # Set to False when you have real API key
    
    if USE_MOCK_DATA:
        print("📋 [DEMO MODE] Using mock data - replace with real API when available")
        mock_data = create_mock_data()
        print()
    else:
        # Initialize client with your API key
        API_KEY = "your_sixtyfour_api_key_here"  # Replace with actual key
        client = SixtyfourClient(API_KEY)
    
    # Example 1: Research Pylon (hackathon sponsor)
    print("🚀 PYLON INTELLIGENCE REPORT")
    print("=" * 50)
    
    if USE_MOCK_DATA:
        pylon_intel = mock_data["Pylon"]
    else:
        pylon_intel = client.enrich_company("Pylon", {"industry": "AI customer support"})
    
    if pylon_intel:
        print(f"🏢 Company: {pylon_intel.name}")
        print(f"🌐 Website: {pylon_intel.website}")
        print(f"📧 Contact: {pylon_intel.email}")
        print(f"🏭 Industry: {pylon_intel.industry}")
        print(f"👥 Team Size: {pylon_intel.employee_count}")
        print(f"💰 Revenue Est: {pylon_intel.revenue_estimate}")
        print(f"🚀 Funding: {pylon_intel.funding_status}")
        print(f"⚙️  Tech Stack: {', '.join(pylon_intel.tech_stack[:6])}")
        print(f"🎯 Key Contacts:")
        for contact in pylon_intel.key_contacts:
            print(f"   • {contact}")
        print(f"🥊 Competitors: {', '.join(pylon_intel.competitive_threats[:4])}")
        print(f"📝 Intelligence Summary:")
        print(f"   {pylon_intel.notes[:400]}...")
        print()
    
    # Example 2: Research Brex (hackathon host)
    print("🏦 BREX INTELLIGENCE REPORT")
    print("=" * 50)
    
    if USE_MOCK_DATA:
        brex_intel = mock_data["Brex"]
    else:
        brex_intel = client.enrich_company("Brex", {"industry": "fintech"})
        
    if brex_intel:
        print(f"🏢 Company: {brex_intel.name}")
        print(f"🌐 Website: {brex_intel.website}")
        print(f"📧 Contact: {brex_intel.email}")
        print(f"🏭 Industry: {brex_intel.industry}")
        print(f"👥 Team Size: {brex_intel.employee_count}")
        print(f"💰 Revenue Est: {brex_intel.revenue_estimate}")
        print(f"🚀 Funding: {brex_intel.funding_status}")
        print(f"⚙️  Tech Stack: {', '.join(brex_intel.tech_stack[:6])}")
        print(f"🎯 Key Contacts:")
        for contact in brex_intel.key_contacts:
            print(f"   • {contact}")
        print(f"🥊 Competitors: {', '.join(brex_intel.competitive_threats[:4])}")
        print(f"📝 Intelligence Summary:")
        print(f"   {brex_intel.notes[:400]}...")
        print()
    
    # Example 3: Competitive threat analysis
    print("⚠️  COMPETITIVE THREAT ANALYSIS")
    print("=" * 50)
    
    if USE_MOCK_DATA:
        companies = {"Pylon": mock_data["Pylon"], "Brex": mock_data["Brex"]}
    else:
        companies = {
            "Pylon": client.enrich_company("Pylon"),
            "Brex": client.enrich_company("Brex")
        }
    
    for name, intel in companies.items():
        if intel:
            threat_level = calculate_threat_level(intel)
            print(f"🏢 {name}")
            print(f"   Threat Level: {threat_level}")
            print(f"   Funding Status: {intel.funding_status}")
            print(f"   Market Position: Strong in {intel.industry}")
            print(f"   Tech Sophistication: {len(intel.tech_stack)} technologies identified")
            print()
    
    print("✅ AUTONOMOUS ACTIONS RECOMMENDED:")
    print("=" * 50)
    print("🤖 Based on intelligence gathered, the agent would:")
    print("   • Monitor Pylon's customer support AI advancements")
    print("   • Track Brex's expansion into new financial products") 
    print("   • Set alerts for funding announcements from competitors")
    print("   • Auto-research any new hires in their engineering teams")
    print("   • Watch for technology stack changes that signal pivots")
    print("\n🎯 This is the kind of intelligence your startup autopilot will gather!")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()