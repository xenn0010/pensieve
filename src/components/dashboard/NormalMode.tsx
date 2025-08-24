import React from 'react';
import { BarChart3, Signal, Building2, Zap } from 'lucide-react';
import ScenarioSwitcher from './ScenarioSwitcher';

const NormalMode: React.FC = () => {
  const sections = [
    {
      icon: Signal,
      title: 'Market Signals',
      description: 'Real-time market intelligence and alerts',
      color: 'bg-blue-500/20 border-blue-500/30'
    },
    {
      icon: Building2,
      title: 'Vendor Management',
      description: 'Track and manage vendor relationships',
      color: 'bg-green-500/20 border-green-500/30'
    },
    {
      icon: Zap,
      title: 'Action Items',
      description: 'Pending tasks and follow-ups',
      color: 'bg-yellow-500/20 border-yellow-500/30'
    },
    {
      icon: BarChart3,
      title: 'Analytics',
      description: 'Performance metrics and insights',
      color: 'bg-purple-500/20 border-purple-500/30'
    }
  ];

  return (
    <div className="p-6">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">
          Dashboard Overview
        </h2>
        <p className="text-dark-300">
          Standard dashboard view with key metrics and insights
        </p>
      </div>

      {/* Financial Scenario Switcher */}
      <ScenarioSwitcher onScenarioChange={() => {}} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {sections.map((section) => (
          <div
            key={section.title}
            className={`p-6 rounded-xl border ${section.color} hover:scale-105 transition-transform duration-200 cursor-pointer`}
          >
            <div className="flex items-center gap-4 mb-4">
              <div className={`p-3 rounded-lg ${section.color.replace('bg-', 'bg-').replace('/20', '/30')}`}>
                <section.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-white">
                {section.title}
              </h3>
            </div>
            <p className="text-dark-200">
              {section.description}
            </p>
          </div>
        ))}
      </div>

      <div className="mt-8 p-6 bg-dark-800/50 rounded-xl border border-dark-700">
        <h3 className="text-lg font-semibold text-white mb-4">
          Recent Activity
        </h3>
        <div className="space-y-3">
          <div className="flex items-center gap-3 text-sm text-dark-300">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>New market signal detected for TechCorp Inc</span>
            <span className="text-xs text-dark-400">2 hours ago</span>
          </div>
          <div className="flex items-center gap-3 text-sm text-dark-300">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span>Vendor assessment completed for GreenEnergy Ltd</span>
            <span className="text-xs text-dark-400">4 hours ago</span>
          </div>
          <div className="flex items-center gap-3 text-sm text-dark-300">
            <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
            <span>Action item due: Review quarterly vendor performance</span>
            <span className="text-xs text-dark-400">1 day ago</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NormalMode;
