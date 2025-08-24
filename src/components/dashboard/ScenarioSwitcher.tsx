import React, { useState, useEffect } from 'react';
import { RefreshCw, TrendingUp, TrendingDown, AlertTriangle, Calendar } from 'lucide-react';
import { API_CONFIG } from '../../config/api';
import { FinancialScenario } from '../../types/financial';

interface ScenarioSwitcherProps {
  onScenarioChange: (scenario: FinancialScenario) => void;
}

const ScenarioSwitcher: React.FC<ScenarioSwitcherProps> = ({ onScenarioChange }) => {
  const [scenarios, setScenarios] = useState<FinancialScenario[]>([]);
  const [activeScenario, setActiveScenario] = useState<string>('healthy_saas');
  const [loading, setLoading] = useState(false);

  // Fetch available scenarios
  const fetchScenarios = async () => {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.FINANCIAL_SCENARIOS}`);
      if (!response.ok) {
        throw new Error('Failed to fetch scenarios');
      }
      
      const data = await response.json();
      setScenarios(data.scenarios);
    } catch (err) {
      console.error('Error fetching scenarios:', err);
    }
  };

  // Switch to a different scenario
  const switchScenario = async (scenarioId: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.FINANCIAL_SCENARIO_SWITCH}/${scenarioId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('Failed to switch scenario');
      }
      
      const data = await response.json();
      setActiveScenario(scenarioId);
      onScenarioChange(data.scenario);
      
      // Refresh the page to show new data
      window.location.reload();
    } catch (err) {
      console.error('Error switching scenario:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScenarios();
  }, []);

  const getScenarioIcon = (scenarioId: string) => {
    switch (scenarioId) {
      case 'healthy_saas':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'cash_crunch':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'rapid_burn':
        return <TrendingDown className="w-4 h-4 text-orange-500" />;
      case 'seasonal_business':
        return <Calendar className="w-4 h-4 text-blue-500" />;
      default:
        return <RefreshCw className="w-4 h-4 text-gray-500" />;
    }
  };

  const getScenarioColor = (scenarioId: string) => {
    switch (scenarioId) {
      case 'healthy_saas':
        return 'border-green-500/30 bg-green-500/10';
      case 'cash_crunch':
        return 'border-red-500/30 bg-red-500/10';
      case 'rapid_burn':
        return 'border-orange-500/30 bg-orange-500/10';
      case 'seasonal_business':
        return 'border-blue-500/30 bg-blue-500/10';
      default:
        return 'border-gray-500/30 bg-gray-500/10';
    }
  };

  if (scenarios.length === 0) {
    return null;
  }

  return (
    <div className="mb-6 p-4 bg-dark-800/50 rounded-xl border border-dark-700">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Financial Scenarios</h3>
          <p className="text-sm text-dark-300">Switch between different financial situations for demo</p>
        </div>
        <button
          onClick={() => fetchScenarios()}
          className="p-2 text-dark-300 hover:text-white transition-colors"
          title="Refresh scenarios"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {scenarios.map((scenario) => (
          <button
            key={scenario.id}
            onClick={() => switchScenario(scenario.id)}
            disabled={loading || scenario.id === activeScenario}
            className={`p-3 rounded-lg border transition-all duration-200 ${
              scenario.id === activeScenario
                ? 'border-green-500/50 bg-green-500/20 scale-105'
                : getScenarioColor(scenario.id)
            } hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            <div className="flex items-center gap-2 mb-2">
              {getScenarioIcon(scenario.id)}
              <span className="text-sm font-medium text-white">
                {scenario.name}
              </span>
            </div>
            
            <div className="text-xs text-dark-300 text-left">
              <div className="mb-1">{scenario.description}</div>
              <div className="grid grid-cols-2 gap-1 text-xs">
                <div>
                  <span className="text-dark-400">Runway:</span>
                  <span className="text-white ml-1">{scenario.runway_months.toFixed(1)}m</span>
                </div>
                <div>
                  <span className="text-dark-400">Cash:</span>
                  <span className="text-white ml-1">${(scenario.cash_on_hand / 1000000).toFixed(1)}M</span>
                </div>
              </div>
            </div>
            
            {scenario.id === activeScenario && (
              <div className="mt-2 text-xs text-green-400 font-medium">
                ✓ Active
              </div>
            )}
          </button>
        ))}
      </div>
      
      {loading && (
        <div className="mt-4 text-center">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-green-500 mx-auto"></div>
          <p className="text-sm text-dark-300 mt-2">Switching scenario...</p>
        </div>
      )}
    </div>
  );
};

export default ScenarioSwitcher;
