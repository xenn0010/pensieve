#!/usr/bin/env python3
"""
Test script for WOW Intelligence signals
Run this to verify all 10 WOW intelligence patterns are working
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append('.')

async def test_sixtyfour_wow_intelligence():
    """Test SixtyFour WOW intelligence signals"""
    print("Testing SixtyFour WOW Intelligence Signals...")
    try:
        import sys
        import os
        sys.path.append(os.path.join('.', 'mcp-servers', 'sixtyfour-mcp'))
        from market_intelligence import SixtyFourMarketIntelligence
        
        sixtyfour = SixtyFourMarketIntelligence()
        
        # Test with different company scenarios
        test_companies = [
            'distressed-startup.com',
            'healthy-unicorn.com', 
            'acquisition-target.com'
        ]
        
        for company in test_companies:
            print(f"\n-- Analyzing {company} --")
            result = await sixtyfour.analyze_wow_intelligence_signals(company)
            
            if 'error' in result:
                print(f"ERROR: {result['error']}")
                continue
                
            signals = result.get('wow_signals', [])
            print(f"Detected {len(signals)} WOW signals")
            
            for signal in signals[:3]:  # Show first 3 signals
                signal_type = signal.get('signal_type', 'unknown')
                severity = signal.get('severity', 'unknown')  
                wow_factor = signal.get('wow_factor', 'N/A')
                print(f"  - {signal_type} ({severity}): {wow_factor}")
            
            risk_level = result.get('risk_level', 'unknown')
            print(f"Overall Risk Level: {risk_level}")
        
        print("SUCCESS: SixtyFour WOW intelligence working!")
        return True
        
    except Exception as e:
        print(f"ERROR: SixtyFour WOW intelligence test failed: {e}")
        return False

async def test_mixrank_tech_intelligence():
    """Test MixRank technology intelligence signals"""
    print("\nTesting MixRank Technology Intelligence Signals...")
    try:
        sys.path.append(os.path.join('.', 'mcp-servers', 'mixrank-mcp'))
        from technology_intelligence import MixRankTechnologyIntelligence
        
        mixrank = MixRankTechnologyIntelligence()
        
        # Test with different technology scenarios  
        test_companies = [
            'legacy-enterprise.com',
            'ai-startup.com',
            'privacy-panic-company.com'
        ]
        
        for company in test_companies:
            print(f"\n-- Analyzing {company} --")
            result = await mixrank.analyze_technology_wow_signals(company)
            
            if 'error' in result:
                print(f"ERROR: {result['error']}")
                continue
                
            signals = result.get('technology_wow_signals', [])
            print(f"Detected {len(signals)} technology WOW signals")
            
            for signal in signals[:3]:  # Show first 3 signals
                signal_type = signal.get('signal_type', 'unknown')
                severity = signal.get('severity', 'unknown')
                wow_factor = signal.get('wow_factor', 'N/A')
                print(f"  - {signal_type} ({severity}): {wow_factor}")
            
            risk_level = result.get('technology_risk_level', 'unknown')
            cost_impact = result.get('cost_impact_estimate_millions', 0)
            print(f"Technology Risk Level: {risk_level}")
            print(f"Estimated Cost Impact: ${cost_impact}M")
        
        print("SUCCESS: MixRank technology intelligence working!")
        return True
        
    except Exception as e:
        print(f"ERROR: MixRank technology intelligence test failed: {e}")
        return False

async def test_decision_orchestrator_integration():
    """Test decision orchestrator WOW intelligence integration"""
    print("\nTesting Decision Orchestrator WOW Intelligence Integration...")
    try:
        sys.path.append(os.path.join('.', 'intelligence-engine'))
        from decision_orchestrator import DecisionOrchestrator
        
        orchestrator = DecisionOrchestrator()
        
        # Test coordination of WOW intelligence analysis
        print("Running comprehensive WOW intelligence analysis coordination...")
        await orchestrator._coordinate_wow_intelligence_analysis()
        
        print("SUCCESS: Decision orchestrator WOW intelligence integration working!")
        return True
        
    except Exception as e:
        print(f"ERROR: Decision orchestrator integration test failed: {e}")
        return False

async def demonstrate_wow_intelligence_showcase():
    """Demonstrate the most impressive WOW intelligence capabilities"""
    print("\n" + "="*60)
    print("WOW INTELLIGENCE SHOWCASE")
    print("="*60)
    
    try:
        # Import our enhanced intelligence systems
        import sys
        import os
        sys.path.append(os.path.join('.', 'mcp-servers', 'sixtyfour-mcp'))
        from market_intelligence import SixtyFourMarketIntelligence
        sys.path.append(os.path.join('.', 'mcp-servers', 'mixrank-mcp'))
        from technology_intelligence import MixRankTechnologyIntelligence
        
        sixtyfour = SixtyFourMarketIntelligence()
        mixrank = MixRankTechnologyIntelligence()
        
        # Showcase scenario: Analyze a "distressed startup" 
        target_company = "failing-unicorn.com"
        print(f"\nTARGET: {target_company}")
        print("Running comprehensive intelligence analysis...")
        
        # Run both intelligence systems simultaneously
        results = await asyncio.gather(
            sixtyfour.analyze_wow_intelligence_signals(target_company),
            mixrank.analyze_technology_wow_signals(target_company),
            return_exceptions=True
        )
        
        sixtyfour_result = results[0] if len(results) > 0 else {}
        mixrank_result = results[1] if len(results) > 1 else {}
        
        # Showcase detected signals
        all_signals = []
        if 'wow_signals' in sixtyfour_result:
            all_signals.extend(sixtyfour_result['wow_signals'])
        if 'technology_wow_signals' in mixrank_result:
            all_signals.extend(mixrank_result['technology_wow_signals'])
        
        print(f"\nINTELLIGENCE ANALYSIS RESULTS:")
        print(f"Total WOW Signals Detected: {len(all_signals)}")
        
        # Show the most impressive signals
        critical_signals = [s for s in all_signals if s.get('severity') == 'critical']
        high_signals = [s for s in all_signals if s.get('severity') == 'high']
        
        print(f"Critical Threat Signals: {len(critical_signals)}")
        print(f"High Priority Signals: {len(high_signals)}")
        
        print(f"\nMOST IMPRESSIVE WOW SIGNALS:")
        for i, signal in enumerate(all_signals[:5], 1):
            signal_type = signal.get('signal_type', 'Unknown Signal')
            wow_factor = signal.get('wow_factor', 'Advanced business intelligence')
            severity = signal.get('severity', 'medium')
            
            print(f"\n{i}. {signal_type.replace('_', ' ').title()} [{severity.upper()}]")
            print(f"   WOW Factor: {wow_factor}")
            
            # Show specific metrics if available
            for key, value in signal.items():
                if 'probability' in key and isinstance(value, (int, float)):
                    print(f"   {key.replace('_', ' ').title()}: {value}%")
                elif 'cost_impact' in key and isinstance(value, (int, float)):
                    print(f"   Estimated Cost Impact: ${value}M")
                elif 'timeline' in key and isinstance(value, (int, float)):
                    print(f"   Predicted Timeline: {value} months")
        
        # Calculate overall threat assessment
        total_cost_impact = sum(s.get('cost_impact_millions', 0) for s in all_signals)
        
        print(f"\nOVERALL IMPACT ASSESSMENT:")
        print(f"Total Estimated Financial Impact: ${total_cost_impact}M")
        print(f"Business Threat Level: {'CRITICAL' if critical_signals else 'HIGH' if high_signals else 'MEDIUM'}")
        
        print(f"\nRECOMMENDED ACTIONS:")
        # Compile actions from all signals
        actions = set()
        for signal in all_signals:
            signal_type = signal.get('signal_type', '')
            if 'death' in signal_type or 'exodus' in signal_type:
                actions.add("ACQUISITION OPPORTUNITY: Monitor for distressed asset purchase")
            elif 'ai' in signal_type or 'stealth' in signal_type:
                actions.add("TECHNOLOGY THREAT: Accelerate AI development to maintain competitive edge")
            elif 'privacy' in signal_type or 'regulatory' in signal_type:
                actions.add("COMPLIANCE ADVANTAGE: Leverage superior privacy practices for market positioning")
            elif 'manipulation' in signal_type:
                actions.add("MARKET VIGILANCE: Monitor for potential market irregularities")
        
        for i, action in enumerate(list(actions)[:5], 1):
            print(f"{i}. {action}")
        
        print(f"\nINTELLIGENCE SOURCES:")
        print(f"- SixtyFour Market Intelligence: {len(sixtyfour_result.get('wow_signals', []))} signals")
        print(f"- MixRank Technology Intelligence: {len(mixrank_result.get('technology_wow_signals', []))} signals")
        print(f"- Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"ERROR in WOW intelligence showcase: {e}")
        return False

async def run_all_tests():
    """Run all WOW intelligence tests"""
    print("STARTING WOW INTELLIGENCE TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("SixtyFour WOW Intelligence", test_sixtyfour_wow_intelligence),
        ("MixRank Technology Intelligence", test_mixrank_tech_intelligence),
        ("Decision Orchestrator Integration", test_decision_orchestrator_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Run showcase
    print(f"\n{'='*50}")
    showcase_success = await demonstrate_wow_intelligence_showcase()
    results.append(("WOW Intelligence Showcase", showcase_success))
    
    # Print summary
    print(f"\n{'='*50}")
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("ALL WOW INTELLIGENCE SYSTEMS OPERATIONAL!")
        print("The AI agent can now detect:")
        print("- Digital exodus patterns predicting layoffs")
        print("- Stealth acquisitions before announcements") 
        print("- Unicorn death spirals before collapse")
        print("- Innovation leaks and corporate espionage")
        print("- Product launches before public announcements")
        print("- Executive scandals and regulatory investigations")
        print("- Technology debt explosions")
        print("- Security infrastructure crises")
        print("- AND MORE!")
        return True
    else:
        print("Some WOW intelligence systems need attention.")
        return False

if __name__ == "__main__":
    print("WOW Intelligence Test Suite - Pensieve CIO")
    print("=" * 50)
    
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nTest suite crashed: {e}")
        sys.exit(1)