import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { KPI } from '../../types/kpi';
import { useGodmodeStore } from '../../store/godmodeStore';

const KPICards: React.FC = () => {
  const { isActive } = useGodmodeStore();
  
  const kpis: KPI[] = [
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
  ];

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
