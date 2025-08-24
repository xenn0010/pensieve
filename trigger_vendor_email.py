#!/usr/bin/env python3
"""
Quick test to trigger vendor negotiation email for yeabsiramullugeta67@gmail.com
"""

import asyncio
import aiohttp
from datetime import datetime

# IFTTT webhook configuration
IFTTT_WEBHOOK_KEY = "your_webhook_key_here"  # Replace with your actual IFTTT webhook key
IFTTT_WEBHOOK_URL = f"https://maker.ifttt.com/trigger/vendor_negotiation_email/with/key/{IFTTT_WEBHOOK_KEY}"
TARGET_EMAIL = "yeabsiramullugeta67@gmail.com"

async def trigger_vendor_negotiation_email():
    """Trigger vendor negotiation email via IFTTT webhook"""
    
    # Email content
    subject = "🎯 URGENT: Vendor Negotiation Opportunity - Salesforce Contract"
    
    body = f"""
📧 VENDOR NEGOTIATION ALERT

🔴 Urgency Level: HIGH

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 VENDOR: Salesforce
📧 Contact: enterprise@salesforce.com
💰 Current Contract Value: $120,000.00
💵 Proposed Savings: $25,000.00 (20.8% reduction)
📅 Contract Expiry: 2024-03-15

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 KEY NEGOTIATION POINTS:

1. Reduce user licenses by 20% due to remote work optimization
2. Negotiate multi-year discount for 3-year commitment  
3. Request additional features at current price point
4. Leverage competitive pricing from HubSpot alternative

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

    # IFTTT webhook payload
    webhook_data = {
        "value1": subject,
        "value2": body,
        "value3": TARGET_EMAIL
    }
    
    print(f"🚀 Triggering vendor negotiation email to {TARGET_EMAIL}...")
    print(f"📧 Subject: {subject}")
    print(f"🔗 Webhook URL: {IFTTT_WEBHOOK_URL}")
    
    # Send webhook request
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(IFTTT_WEBHOOK_URL, json=webhook_data) as response:
                if response.status == 200:
                    print(f"✅ SUCCESS: Vendor negotiation email triggered successfully!")
                    print(f"📧 Check {TARGET_EMAIL} for the vendor negotiation email")
                    return True
                else:
                    response_text = await response.text()
                    print(f"❌ FAILED: Webhook returned status {response.status}")
                    print(f"📄 Response: {response_text}")
                    return False
        except Exception as e:
            print(f"❌ ERROR: Failed to send webhook request: {e}")
            return False

async def setup_instructions():
    """Display IFTTT setup instructions"""
    
    print("🔧 IFTTT Setup Instructions")
    print("=" * 50)
    print("""
To make this work, you need to set up IFTTT:

1. 🌐 Go to https://ifttt.com and create an account
2. 📱 Create a new applet: https://ifttt.com/create
3. 🔗 Choose 'Webhooks' as the trigger service
4. 📝 Set event name: 'vendor_negotiation_email'
5. 📧 Choose 'Email' as the action service
6. ⚙️  Configure the email action:
   - To address: yeabsiramullugeta67@gmail.com
   - Subject: {{Value1}}
   - Body: {{Value2}}
7. 🔑 Get your webhook key from: https://ifttt.com/maker_webhooks/settings
8. 📝 Replace 'your_webhook_key_here' in this script with your real key

🔗 Your webhook URL will be:
https://maker.ifttt.com/trigger/vendor_negotiation_email/with/key/YOUR_ACTUAL_KEY
""")

async def main():
    """Main function"""
    
    print("🎯 Vendor Negotiation Email Trigger")
    print("Sending email to yeabsiramullugeta67@gmail.com")
    print("=" * 60)
    
    # Check if webhook key is configured
    if IFTTT_WEBHOOK_KEY == "your_webhook_key_here":
        print("⚠️  WARNING: IFTTT webhook key not configured!")
        await setup_instructions()
        print("\n🧪 Running in DEMO MODE (email won't actually send)")
        print("   Update IFTTT_WEBHOOK_KEY variable with your real key to send emails")
    
    # Trigger the email
    success = await trigger_vendor_negotiation_email()
    
    if success:
        print(f"\n🎉 Email trigger completed successfully!")
        print(f"📧 Vendor negotiation email should arrive at {TARGET_EMAIL}")
    else:
        print(f"\n💥 Email trigger failed - check your IFTTT configuration")
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        if success:
            print("\n✅ Process completed successfully")
        else:
            print("\n❌ Process failed")
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
