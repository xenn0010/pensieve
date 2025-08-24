#!/usr/bin/env python3
"""
Vendor Negotiation Email System with IFTTT Integration
Automatically triggers vendor negotiation emails via IFTTT webhooks
"""

import asyncio
import json
import aiohttp
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

# IFTTT Webhook Configuration
IFTTT_WEBHOOK_URL = "https://maker.ifttt.com/trigger/{event_name}/with/key/{webhook_key}"

@dataclass
class VendorNegotiationEmail:
    """Vendor negotiation email data structure"""
    vendor_name: str
    contact_email: str
    current_contract_value: float
    proposed_savings: float
    negotiation_points: List[str]
    urgency_level: str  # low, medium, high
    contract_expiry_date: str
    
class VendorNegotiationSystem:
    """Automated vendor negotiation email system"""
    
    def __init__(self, ifttt_webhook_key: str):
        self.webhook_key = ifttt_webhook_key
        self.target_email = "yeabsiramullugeta67@gmail.com"
    
    async def trigger_vendor_negotiation_email(self, vendor_data: VendorNegotiationEmail):
        """Trigger vendor negotiation email via IFTTT webhook"""
        
        # Prepare email content
        email_subject = f"🎯 Vendor Negotiation Opportunity: {vendor_data.vendor_name}"
        
        email_body = self._generate_negotiation_email_content(vendor_data)
        
        # IFTTT webhook payload
        webhook_data = {
            "value1": email_subject,
            "value2": email_body,
            "value3": self.target_email
        }
        
        # Send webhook to IFTTT
        webhook_url = IFTTT_WEBHOOK_URL.format(
            event_name="vendor_negotiation_email",
            webhook_key=self.webhook_key
        )
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(webhook_url, json=webhook_data) as response:
                    if response.status == 200:
                        print(f"✅ Successfully triggered vendor negotiation email for {vendor_data.vendor_name}")
                        return True
                    else:
                        print(f"❌ Failed to trigger webhook: {response.status}")
                        return False
            except Exception as e:
                print(f"❌ Error sending webhook: {e}")
                return False
    
    def _generate_negotiation_email_content(self, vendor_data: VendorNegotiationEmail) -> str:
        """Generate comprehensive vendor negotiation email content"""
        
        urgency_emoji = {
            "low": "🟢",
            "medium": "🟡", 
            "high": "🔴"
        }
        
        savings_percentage = (vendor_data.proposed_savings / vendor_data.current_contract_value) * 100
        
        email_content = f"""
📧 VENDOR NEGOTIATION OPPORTUNITY ALERT

{urgency_emoji.get(vendor_data.urgency_level, '🟡')} Urgency Level: {vendor_data.urgency_level.upper()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 VENDOR: {vendor_data.vendor_name}
📧 Contact: {vendor_data.contact_email}
💰 Current Contract Value: ${vendor_data.current_contract_value:,.2f}
💵 Proposed Savings: ${vendor_data.proposed_savings:,.2f} ({savings_percentage:.1f}% reduction)
📅 Contract Expiry: {vendor_data.contract_expiry_date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 KEY NEGOTIATION POINTS:
"""
        
        for i, point in enumerate(vendor_data.negotiation_points, 1):
            email_content += f"\n{i}. {point}"
        
        email_content += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 RECOMMENDED ACTIONS:
• Schedule negotiation call within 48 hours
• Prepare competitive quotes from alternatives
• Review contract terms for optimization opportunities
• Document all negotiation outcomes

⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🤖 Triggered by: Pensieve Autonomous CIO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return email_content.strip()
    
    async def analyze_vendor_opportunities(self) -> List[VendorNegotiationEmail]:
        """Analyze current vendors for negotiation opportunities"""
        
        # Mock vendor data - in production, this would come from your vendor management system
        vendor_opportunities = [
            VendorNegotiationEmail(
                vendor_name="Salesforce",
                contact_email="enterprise@salesforce.com",
                current_contract_value=120000.0,
                proposed_savings=25000.0,
                negotiation_points=[
                    "Reduce user licenses by 20% due to remote work optimization",
                    "Negotiate multi-year discount for 3-year commitment",
                    "Request additional features at current price point",
                    "Leverage competitive pricing from HubSpot alternative"
                ],
                urgency_level="high",
                contract_expiry_date="2024-03-15"
            ),
            VendorNegotiationEmail(
                vendor_name="AWS",
                contact_email="enterprise@aws.com", 
                current_contract_value=85000.0,
                proposed_savings=15000.0,
                negotiation_points=[
                    "Optimize reserved instance commitments",
                    "Negotiate enterprise discount tier",
                    "Review storage costs and archival options",
                    "Consolidate services for volume pricing"
                ],
                urgency_level="medium",
                contract_expiry_date="2024-06-30"
            ),
            VendorNegotiationEmail(
                vendor_name="Slack",
                contact_email="sales@slack.com",
                current_contract_value=45000.0,
                proposed_savings=8000.0,
                negotiation_points=[
                    "Reduce per-user pricing for annual commitment",
                    "Bundle with additional Salesforce products",
                    "Negotiate guest user limitations removal",
                    "Request premium features at standard tier"
                ],
                urgency_level="low",
                contract_expiry_date="2024-09-01"
            )
        ]
        
        return vendor_opportunities


async def setup_ifttt_integration():
    """Setup IFTTT integration for vendor negotiation emails"""
    
    print("🔧 Setting up IFTTT Integration for Vendor Negotiation Emails")
    print("=" * 60)
    
    print("""
📧 IFTTT Setup Instructions:

1. Go to IFTTT.com and create account
2. Create new applet: https://ifttt.com/create
3. Choose 'Webhooks' as trigger service
4. Event name: 'vendor_negotiation_email'
5. Choose 'Email' as action service
6. Configure email action:
   - To: yeabsiramullugeta67@gmail.com
   - Subject: {{Value1}}
   - Body: {{Value2}}
7. Get your webhook key from: https://ifttt.com/maker_webhooks/settings

Your webhook URL will be:
https://maker.ifttt.com/trigger/vendor_negotiation_email/with/key/YOUR_WEBHOOK_KEY
""")
    
    # For demo purposes, we'll use a placeholder key
    demo_webhook_key = "your_ifttt_webhook_key_here"
    
    print(f"\n🧪 Testing with demo webhook key: {demo_webhook_key}")
    
    return demo_webhook_key


async def main():
    """Main function to demonstrate vendor negotiation email system"""
    
    print("🎯 Vendor Negotiation Email System")
    print("Automatically trigger negotiation emails via IFTTT webhooks")
    print("=" * 70)
    
    # Setup IFTTT integration
    webhook_key = await setup_ifttt_integration()
    
    # Initialize vendor negotiation system
    vendor_system = VendorNegotiationSystem(webhook_key)
    
    # Analyze vendor opportunities
    print("\n📊 Analyzing vendor negotiation opportunities...")
    vendor_opportunities = await vendor_system.analyze_vendor_opportunities()
    
    print(f"\n✅ Found {len(vendor_opportunities)} vendor negotiation opportunities:")
    
    for i, vendor in enumerate(vendor_opportunities, 1):
        savings_percent = (vendor.proposed_savings / vendor.current_contract_value) * 100
        print(f"   {i}. {vendor.vendor_name}: ${vendor.proposed_savings:,.0f} savings ({savings_percent:.1f}%)")
    
    # Trigger emails for high-priority vendors
    print(f"\n📧 Triggering vendor negotiation emails to {vendor_system.target_email}...")
    
    high_priority_vendors = [v for v in vendor_opportunities if v.urgency_level == "high"]
    
    for vendor in high_priority_vendors:
        print(f"\n🚀 Triggering email for {vendor.vendor_name}...")
        success = await vendor_system.trigger_vendor_negotiation_email(vendor)
        
        if success:
            print(f"   ✅ Email triggered successfully")
        else:
            print(f"   ❌ Failed to trigger email")
    
    print(f"\n🎉 Vendor negotiation email system demo complete!")
    print(f"📧 Check {vendor_system.target_email} for vendor negotiation emails")
    
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        print("\n✅ System completed successfully")
    except KeyboardInterrupt:
        print("\n❌ System interrupted by user")
    except Exception as e:
        print(f"\n💥 System error: {e}")
