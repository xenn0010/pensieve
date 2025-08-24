import React, { useEffect, useState } from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { KPI } from '../../types/kpi';
import { useGodmodeStore } from '../../store/godmodeStore';
import { API_CONFIG } from '../../config/api';

const KPICards: React.FC = () => {
  const { isActive } = useGodmodeStore();
  const [kpis, setKpis] = useState<KPI[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch financial KPIs from API
  const fetchFinancialKPIs = async () => {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.FINANCIAL_KPIS}`);
      if (!response.ok) {
        throw new Error('Failed to fetch financial data');
      }
      
      const data = await response.json();
      
      // Transform API data to KPI format
      const transformedKPIs: KPI[] = [
        {
          label: 'Runway Months',
          value: data.runway_months.toFixed(1),
          change: data.trends.runway_change,
          trend: data.trends.runway_change > 0 ? 'up' : data.trends.runway_change < 0 ? 'down' : 'stable',
          unit: 'months',
          description: 'Time until cash runs out',
          color: 'text-green-400'
        },
        {
          label: 'Cash on Hand',
          value: `$${(data.cash_on_hand / 1000000).toFixed(1)}M`,
          change: data.trends.cash_change,
          trend: data.trends.cash_change > 0 ? 'up' : data.trends.cash_change < 0 ? 'down' : 'stable',
          unit: 'USD',
          description: 'Available liquid funds',
          color: 'text-blue-400'
        },
        {
          label: 'Monthly Burn',
          value: `$${(data.monthly_burn / 1000).toFixed(0)}K`,
          change: data.trends.burn_change,
          trend: data.trends.burn_change > 0 ? 'up' : data.trends.burn_change < 0 ? 'down' : 'stable',
          unit: 'USD',
          description: 'Monthly cash consumption',
          color: 'text-yellow-400'
        }
      ];
      
      setKpis(transformedKPIs);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching financial KPIs:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      setLoading(false);
      
      // Fallback to mock data
      setKpis([
        {
          label: 'Runway Months',
          value: '18.5',
          change: 2.3,
          trend: 'up',
          unit: 'months',
          description: 'Time until cash runs out',
          color: 'text-green-400'
        },
        {
          label: 'Cash on Hand',
          value: '$2.4M',
          change: -0.8,
          trend: 'down',
          unit: 'USD',
          description: 'Available liquid funds',
          color: 'text-blue-400'
        },
        {
          label: 'Monthly Burn',
          value: '$130K',
          change: 0,
          trend: 'stable',
          unit: 'USD',
          description: 'Monthly cash consumption',
          color: 'text-yellow-400'
        }
      ]);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchFinancialKPIs();
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchFinancialKPIs, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const getTrendIcon = (trend: KPI['trend']) => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      default:
        return <Minus className="w-4 h-4 text-gray-500" />;
    }
  };

  const getTrendColor = (trend: KPI['trend']) => {
    switch (trend) {
      case 'up':
        return 'text-green-500';
      case 'down':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  // Show loading state
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[1, 2, 3].map((i) => (
          <div key={i} className="kpi-card backdrop-blur-md border bg-dark-800/20 border-dark-700/50 animate-pulse">
            <div className="h-20 bg-dark-700/30 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="col-span-3 p-4 bg-red-500/20 border border-red-500/30 rounded-xl">
          <p className="text-red-400 text-center">
            ⚠️ Error loading financial data: {error}. Using fallback data.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {kpis.map((kpi) => (
        <div key={kpi.label} className={`kpi-card backdrop-blur-md border ${
          isActive 
            ? 'bg-dark-800/30 border-dark-700/30 shadow-lg shadow-black/20' 
            : 'bg-dark-800/20 border-dark-700/50'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-dark-300">
              {kpi.label}
            </h3>
            {getTrendIcon(kpi.trend)}
          </div>
          
          <div className="mb-1">
            <span className={`text-2xl font-bold ${kpi.color}`}>
              {kpi.value}
            </span>
            <span className="text-sm text-dark-400 ml-1">
              {kpi.unit}
            </span>
          </div>
          
          <div className="flex items-center gap-2">
            <span className={`text-sm ${getTrendColor(kpi.trend)}`}>
              {kpi.change !== undefined && kpi.change !== 0 && (kpi.change > 0 ? '+' : '')}
              {kpi.change !== undefined ? kpi.change : '0'}
            </span>
            <span className="text-xs text-dark-400">
              {kpi.description}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default KPICards;
