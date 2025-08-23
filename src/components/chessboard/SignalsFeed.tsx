import React from 'react';
import { Badge } from '../ui/badge';
import { TrendingUp, TrendingDown, AlertTriangle, Info, Clock } from 'lucide-react';
import { useDemoStore } from '../../lib/demo-store';
import type { Signal } from '../../lib/demo-store';

export const SignalsFeed: React.FC = () => {
  const { store } = useDemoStore();

  const getSignalIcon = (type: Signal['type']) => {
    switch (type) {
      case 'positive':
        return <TrendingUp className="w-4 h-4 text-green-400" />;
      case 'negative':
        return <TrendingDown className="w-4 h-4 text-red-400" />;
      default:
        return <Info className="w-4 h-4 text-blue-400" />;
    }
  };

  const getSignalColor = (type: Signal['type']) => {
    switch (type) {
      case 'positive':
        return 'border-green-600/30 bg-green-600/10';
      case 'negative':
        return 'border-red-600/30 bg-red-600/10';
      default:
        return 'border-blue-600/30 bg-blue-600/10';
    }
  };

  const getCategoryIcon = (category: Signal['category']) => {
    switch (category) {
      case 'financial':
        return '💰';
      case 'competitive':
        return '⚔️';
      case 'market':
        return '📈';
      case 'regulatory':
        return '⚖️';
      case 'operational':
        return '⚙️';
      default:
        return '📊';
    }
  };

  const formatTimestamp = (timestamp: Date) => {
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - timestamp.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    return `${diffInDays}d ago`;
  };

  const getSeverityColor = (severity: number) => {
    if (severity >= 4) return 'text-red-400';
    if (severity >= 3) return 'text-yellow-400';
    return 'text-green-400';
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Clock className="w-4 h-4 text-primary-500" />
        <h4 className="font-medium text-white">Live Market Signals</h4>
        <Badge variant="outline" className="text-xs">
          {store.chessboard.signals.length} active
        </Badge>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto">
        {store.chessboard.signals.map((signal) => (
          <div
            key={signal.id}
            className={`p-3 rounded-lg border transition-colors ${getSignalColor(signal.type)}`}
          >
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 mt-0.5">
                {getSignalIcon(signal.type)}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{getCategoryIcon(signal.category)}</span>
                  <h5 className="text-sm font-medium text-white truncate">
                    {signal.title}
                  </h5>
                  <Badge variant="outline" className={`text-xs ${getSeverityColor(signal.severity)}`}>
                    {signal.severity}/5
                  </Badge>
                </div>
                
                <p className="text-xs text-dark-300 mb-2 line-clamp-2">
                  {signal.description}
                </p>
                
                {signal.impact && (
                  <p className="text-xs text-dark-400 mb-2 italic">
                    Impact: {signal.impact}
                  </p>
                )}
                
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="text-xs">
                      {signal.category}
                    </Badge>
                    {signal.companyName && (
                      <span className="text-dark-400">
                        via {signal.companyName}
                      </span>
                    )}
                  </div>
                  
                  <div className="flex items-center gap-2 text-dark-400">
                    <span>{signal.source}</span>
                    <span>•</span>
                    <span>{formatTimestamp(signal.timestamp)}</span>
                  </div>
                </div>
                
                {signal.relevance && (
                  <div className="mt-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-dark-400">Relevance:</span>
                      <span className="text-white">{signal.relevance}/10</span>
                    </div>
                    <div className="w-full bg-dark-700 rounded-full h-1 mt-1">
                      <div 
                        className="bg-primary-500 h-1 rounded-full" 
                        style={{ width: `${signal.relevance * 10}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {store.chessboard.signals.length === 0 && (
        <div className="text-center py-8 text-dark-400">
          <AlertTriangle className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p className="text-sm">No active signals</p>
          <p className="text-xs mt-1">Market intelligence will appear here</p>
        </div>
      )}
    </div>
  );
};
