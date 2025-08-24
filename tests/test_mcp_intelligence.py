#!/usr/bin/env python3
"""
Test script for MCP Intelligence Systems
Tests SixtyFour and MixRank MCP servers with Gemini orchestration
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Import our MCP servers and orchestrator
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# Add the directory path for mcp-servers (with dashes)
mcp_servers_path = os.path.join(os.path.abspath('.'), 'mcp-servers')
sys.path.insert(0, mcp_servers_path)

# Try to import each module with error handling
try:
    sys.path.insert(0, os.path.join(mcp_servers_path, 'sixtyfour-mcp'))
    from market_intelligence import SixtyFourMarketIntelligence
    print("Successfully imported SixtyFourMarketIntelligence")
except ImportError as e:
    print(f"Failed to import SixtyFourMarketIntelligence: {e}")
    SixtyFourMarketIntelligence = None

try:
    sys.path.insert(0, os.path.join(mcp_servers_path, 'mixrank-mcp'))
    from technology_intelligence import MixRankTechnologyIntelligence
    print("Successfully imported MixRankTechnologyIntelligence")
except ImportError as e:
    print(f"Failed to import MixRankTechnologyIntelligence: {e}")
    MixRankTechnologyIntelligence = None

try:
    sys.path.insert(0, os.path.join(os.path.abspath('.'), 'intelligence-engine'))
    from decision_orchestrator import DecisionOrchestrator, IntelligenceEvent, EventType, Priority
    print("Successfully imported DecisionOrchestrator")
except ImportError as e:
    print(f"Failed to import DecisionOrchestrator: {e}")
    DecisionOrchestrator = None
    IntelligenceEvent = None
    EventType = None
    Priority = None

try:
    sys.path.insert(0, os.path.join(os.path.abspath('.'), 'config'))
    from settings import settings
    print("Successfully imported settings")
except ImportError as e:
    print(f"Failed to import settings: {e}")
    # Create mock settings
    class MockSettings:
        gemini_model = "gemini-pro"
        gemini_api_key = "test-key"
        sixtyfour_api_key = "test-key"
        redis_url = "redis://localhost:6379"
        event_processing_interval = 30
        competitor_threat_threshold = 0.7
    settings = MockSettings()


async def test_sixtyfour_intelligence():
    """Test SixtyFour Market Intelligence MCP Server"""
    print("\n" + "="*60)
    print("🔍 TESTING SIXTYFOUR MARKET INTELLIGENCE")
    print("="*60)
    
    if not SixtyFourMarketIntelligence:
        print("❌ SixtyFourMarketIntelligence not available - skipping test")
        return False
    
    try:
        # Initialize SixtyFour intelligence
        sixtyfour = SixtyFourMarketIntelligence()
        await sixtyfour.initialize()
        
        # Test companies for analysis
        test_companies = [
            'competitor1.com',
            'unicorn-startup.com', 
            'distressed-company.com'
        ]
        
        for company in test_companies:
            print(f"\n🎯 Analyzing {company} with SixtyFour WOW Intelligence...")
            
            # Run comprehensive WOW intelligence analysis
            wow_results = await sixtyfour.analyze_wow_intelligence_signals(company)
            
            if 'error' not in wow_results:
                signals_detected = wow_results.get('wow_signals', [])
                print(f"✅ Analysis Complete: {len(signals_detected)} WOW signals detected")
                
                # Display the most interesting signals
                for i, signal in enumerate(signals_detected[:3], 1):
                    print(f"   {i}. {signal.get('signal_type', 'Unknown')} - "
                          f"Severity: {signal.get('severity', 'medium')} - "
                          f"WOW Factor: {signal.get('wow_factor', 'N/A')}")
                
                # Show risk level and recommended actions
                print(f"📊 Overall Risk Level: {wow_results.get('risk_level', 'unknown')}")
                actions = wow_results.get('recommended_actions', [])
                if actions:
                    print(f"💡 Top Recommended Actions:")
                    for action in actions[:3]:
                        print(f"   • {action}")
            else:
                print(f"❌ Error analyzing {company}: {wow_results['error']}")
        
        print("\n✅ SixtyFour intelligence test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ SixtyFour test failed: {e}")
        return False


async def test_mixrank_intelligence():
    """Test MixRank Technology Intelligence MCP Server"""
    print("\n" + "="*60)
    print("🔧 TESTING MIXRANK TECHNOLOGY INTELLIGENCE")
    print("="*60)
    
    if not MixRankTechnologyIntelligence:
        print("❌ MixRankTechnologyIntelligence not available - skipping test")
        return False
    
    try:
        # Initialize MixRank intelligence
        mixrank = MixRankTechnologyIntelligence()
        await mixrank.initialize()
        
        test_companies = [
            'tech-company.com',
            'ai-startup.com',
            'legacy-corp.com'
        ]
        
        for company in test_companies:
            print(f"\n🎯 Analyzing {company} with MixRank Technology WOW Intelligence...")
            
            # Run technology WOW intelligence analysis
            tech_results = await mixrank.analyze_technology_wow_signals(company)
            
            if 'error' not in tech_results:
                tech_signals = tech_results.get('technology_wow_signals', [])
                print(f"✅ Analysis Complete: {len(tech_signals)} technology WOW signals detected")
                
                # Display interesting technology signals
                for i, signal in enumerate(tech_signals[:3], 1):
                    print(f"   {i}. {signal.get('signal_type', 'Unknown')} - "
                          f"Severity: {signal.get('severity', 'medium')} - "
                          f"Tech Impact: {signal.get('wow_factor', 'N/A')}")
                
                # Show technology risk and recommendations
                print(f"🔧 Technology Risk Level: {tech_results.get('technology_risk_level', 'unknown')}")
                tech_actions = tech_results.get('recommended_technology_actions', [])
                if tech_actions:
                    print(f"🛠️ Top Technology Actions:")
                    for action in tech_actions[:3]:
                        print(f"   • {action}")
            else:
                print(f"❌ Error analyzing {company}: {tech_results['error']}")
        
        print("\n✅ MixRank technology intelligence test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ MixRank test failed: {e}")
        return False


async def test_gemini_orchestration():
    """Test Gemini-powered decision orchestration"""
    print("\n" + "="*60) 
    print("🧠 TESTING GEMINI DECISION ORCHESTRATION")
    print("="*60)
    
    if not DecisionOrchestrator:
        print("❌ DecisionOrchestrator not available - skipping test")
        return False
    
    try:
        # Initialize decision orchestrator
        orchestrator = DecisionOrchestrator()
        
        # Create test intelligence events
        test_events = [
            IntelligenceEvent(
                event_type=EventType.COMPETITIVE_THREAT,
                priority=Priority.HIGH,
                source='wow_intelligence_test',
                data={
                    'company_analyzed': 'competitor1.com',
                    'signals_detected': [
                        {
                            'signal_type': 'digital_exodus_prediction',
                            'severity': 'critical',
                            'exodus_score': 0.85,
                            'wow_factor': 'Predict layoffs before news breaks'
                        }
                    ],
                    'recommended_actions': ['Monitor for acquisition opportunities'],
                    'risk_level': 'high'
                },
                timestamp=datetime.now(),
                context={
                    'runway_days': 180,
                    'customer_count': 1500,
                    'competitive_pressure': 'high'
                }
            ),
            IntelligenceEvent(
                event_type=EventType.MARKET_OPPORTUNITY,
                priority=Priority.MEDIUM,
                source='technology_intelligence_test',
                data={
                    'company_analyzed': 'ai-startup.com',
                    'technology_signals': [
                        {
                            'signal_type': 'stealth_ai_development',
                            'severity': 'high',
                            'ai_capability_probability': 75,
                            'wow_factor': 'Detect secret AI projects before announcement'
                        }
                    ],
                    'recommended_actions': ['Accelerate AI development'],
                    'technology_risk_level': 'medium'
                },
                timestamp=datetime.now(),
                context={
                    'runway_days': 240,
                    'customer_count': 800,
                    'competitive_pressure': 'medium'
                }
            )
        ]
        
        print(f"📤 Testing {len(test_events)} intelligence events with Gemini orchestration...")
        
        # Process each test event
        for i, event in enumerate(test_events, 1):
            print(f"\n🎯 Processing Event {i}: {event.event_type.value}")
            print(f"   Priority: {event.priority.value}")
            print(f"   Source: {event.source}")
            
            # Add event to orchestrator queue
            await orchestrator.add_event(event)
            
            # Process the event
            await orchestrator._process_event(event)
            
            print(f"✅ Event {i} processed successfully by Gemini orchestrator")
        
        # Test comprehensive WOW intelligence analysis coordination
        print(f"\n🎯 Testing comprehensive WOW intelligence coordination...")
        await orchestrator._coordinate_wow_intelligence_analysis()
        
        print("\n✅ Gemini orchestration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Gemini orchestration test failed: {e}")
        return False


async def test_end_to_end_intelligence_flow():
    """Test complete end-to-end intelligence flow"""
    print("\n" + "="*60)
    print("🌟 TESTING END-TO-END INTELLIGENCE FLOW")
    print("="*60)
    
    try:
        # Initialize all systems
        orchestrator = DecisionOrchestrator()
        sixtyfour = SixtyFourMarketIntelligence()
        mixrank = MixRankTechnologyIntelligence()
        
        await sixtyfour.initialize()
        await mixrank.initialize()
        
        target_company = 'target-analysis.com'
        
        print(f"🎯 Running complete intelligence analysis for {target_company}...")
        
        # Step 1: Gather SixtyFour intelligence
        print(f"   Step 1: SixtyFour market intelligence...")
        market_intel = await sixtyfour.analyze_wow_intelligence_signals(target_company)
        
        # Step 2: Gather MixRank technology intelligence  
        print(f"   Step 2: MixRank technology intelligence...")
        tech_intel = await mixrank.analyze_technology_wow_signals(target_company)
        
        # Step 3: Combine intelligence data
        print(f"   Step 3: Combining intelligence data...")
        combined_intelligence = {
            'sixtyfour_intelligence': market_intel,
            'mixrank_intelligence': tech_intel,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Step 4: Process with orchestrator
        print(f"   Step 4: Processing with Gemini orchestrator...")
        await orchestrator._process_combined_intelligence(target_company, combined_intelligence)
        
        # Step 5: Display results
        print(f"\n📊 COMPLETE INTELLIGENCE ANALYSIS RESULTS")
        print(f"="*50)
        
        # Market intelligence results
        market_signals = market_intel.get('wow_signals', [])
        print(f"📈 Market Intelligence: {len(market_signals)} signals detected")
        for signal in market_signals[:2]:
            print(f"   • {signal.get('signal_type', 'Unknown')} ({signal.get('severity', 'medium')})")
        
        # Technology intelligence results  
        tech_signals = tech_intel.get('technology_wow_signals', [])
        print(f"🔧 Technology Intelligence: {len(tech_signals)} tech signals detected")
        for signal in tech_signals[:2]:
            print(f"   • {signal.get('signal_type', 'Unknown')} ({signal.get('severity', 'medium')})")
        
        # Combined risk assessment
        overall_risk = market_intel.get('risk_level', 'unknown')
        tech_risk = tech_intel.get('technology_risk_level', 'unknown') 
        print(f"⚠️ Overall Risk: Market={overall_risk}, Technology={tech_risk}")
        
        # Top recommendations
        all_actions = []
        all_actions.extend(market_intel.get('recommended_actions', [])[:2])
        all_actions.extend(tech_intel.get('recommended_technology_actions', [])[:2])
        
        if all_actions:
            print(f"💡 Top Combined Recommendations:")
            for action in all_actions[:4]:
                print(f"   • {action}")
        
        print(f"\n✅ End-to-end intelligence flow test completed successfully!")
        print(f"🎉 All systems working together: SixtyFour + MixRank + Gemini Orchestration")
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False


async def main():
    """Run all MCP intelligence tests"""
    print("🚀 PENSIEVE MCP INTELLIGENCE SYSTEM TESTS")
    print("=" * 80)
    print(f"Testing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Gemini Model: {settings.gemini_model}")
    print("=" * 80)
    
    test_results = {
        'sixtyfour_intelligence': False,
        'mixrank_intelligence': False, 
        'gemini_orchestration': False,
        'end_to_end_flow': False
    }
    
    # Run all tests
    test_results['sixtyfour_intelligence'] = await test_sixtyfour_intelligence()
    test_results['mixrank_intelligence'] = await test_mixrank_intelligence()
    test_results['gemini_orchestration'] = await test_gemini_orchestration()
    test_results['end_to_end_flow'] = await test_end_to_end_intelligence_flow()
    
    # Final results
    print("\n" + "="*80)
    print("🎯 FINAL TEST RESULTS")
    print("="*80)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! MCP Intelligence System is working perfectly!")
        print("🧠 Gemini orchestration + SixtyFour + MixRank = Ready for production!")
    else:
        print("⚠️ Some tests failed. Review errors above for troubleshooting.")
    
    return passed == total


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    exit(0 if success else 1)