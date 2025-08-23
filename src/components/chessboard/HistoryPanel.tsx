import React from 'react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { History, RotateCcw, Clock, Activity } from 'lucide-react';
import { useDemoStore } from '../../lib/demo-store';

export const HistoryPanel: React.FC = () => {
  const { store } = useDemoStore();

  const formatTimestamp = (timestamp: Date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - timestamp.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    
    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `${diffInHours}h ago`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    return `${diffInDays}d ago`;
  };

  const getActionIcon = (action: string) => {
    if (action.includes('Added')) return '➕';
    if (action.includes('Removed')) return '➖';
    if (action.includes('Duplicated')) return '📋';
    if (action.includes('Created')) return '🆕';
    if (action.includes('Reset')) return '🔄';
    return '📝';
  };

  const getActionColor = (action: string) => {
    if (action.includes('Added') || action.includes('Created')) return 'text-green-400';
    if (action.includes('Removed') || action.includes('Reset')) return 'text-red-400';
    if (action.includes('Duplicated')) return 'text-blue-400';
    return 'text-gray-400';
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <History className="w-4 h-4 text-primary-500" />
          <h4 className="font-medium text-white">Action History</h4>
          <Badge variant="outline" className="text-xs">
            {store.chessboard.history.length} actions
          </Badge>
        </div>
        
        {store.chessboard.history.length > 0 && (
          <Button variant="outline" size="sm" className="text-xs">
            <RotateCcw className="w-3 h-3 mr-1" />
            Clear
          </Button>
        )}
      </div>

      <div className="space-y-2 max-h-80 overflow-y-auto">
        {store.chessboard.history.slice().reverse().map((historyItem, index) => (
          <div
            key={historyItem.id}
            className="p-3 rounded-lg border border-dark-700 bg-dark-800/30 hover:bg-dark-700/30 transition-colors"
          >
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 mt-0.5">
                <span className="text-lg">{getActionIcon(historyItem.action)}</span>
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <p className={`text-sm font-medium ${getActionColor(historyItem.action)}`}>
                    {historyItem.action}
                  </p>
                  {index === 0 && (
                    <Badge variant="default" className="text-xs">
                      Latest
                    </Badge>
                  )}
                </div>
                
                <div className="flex items-center justify-between text-xs">
                  <span className="text-dark-400">
                    {formatTimestamp(historyItem.timestamp)}
                  </span>
                  
                  {historyItem.data && (
                    <Button variant="ghost" size="sm" className="text-xs opacity-50 hover:opacity-100">
                      <RotateCcw className="w-3 h-3 mr-1" />
                      Undo
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {store.chessboard.history.length === 0 && (
        <div className="text-center py-8 text-dark-400">
          <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p className="text-sm">No actions yet</p>
          <p className="text-xs mt-1">Your scenario changes will appear here</p>
        </div>
      )}
      
      {store.chessboard.history.length > 0 && (
        <div className="pt-3 border-t border-dark-700 text-center">
          <Button variant="outline" size="sm" className="text-xs">
            <Clock className="w-3 h-3 mr-1" />
            View Full History
          </Button>
        </div>
      )}
    </div>
  );
};
