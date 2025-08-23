import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { useDemoStore } from '../../lib/demo-store';
import { Zap, Plus, Search, Filter } from 'lucide-react';

export const MoveLibrary: React.FC = () => {
  const { store } = useDemoStore();
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');

  const handleDragStart = (e: React.DragEvent, moveId: string) => {
    e.dataTransfer.setData('text/plain', moveId);
    e.dataTransfer.effectAllowed = 'copy';
  };

  const formatCurrency = (amount: number): string => {
    if (amount >= 1000000) return `$${(amount / 1000000).toFixed(1)}M`;
    if (amount >= 1000) return `$${(amount / 1000).toFixed(0)}k`;
    return `$${amount.toFixed(0)}`;
  };

  const categories = ['all', 'Hiring', 'Cost Control', 'Fundraising', 'Technology', 'Sales', 'Facilities'];
  
  const filteredMoves = store.chessboard.moveLibrary.filter(move => {
    const matchesCategory = selectedCategory === 'all' || move.category === selectedCategory;
    const matchesSearch = move.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         move.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const aiRecommendations = filteredMoves.filter(move => move.isAiRecommended);
  const regularMoves = filteredMoves.filter(move => !move.isAiRecommended);

  return (
    <div className="w-80 h-full bg-dark-800/60 backdrop-blur-md border-r border-dark-700/50 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-dark-700/50">
        <h3 className="text-lg font-semibold text-white mb-4">Move Library</h3>
        
        {/* Search */}
        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-dark-400" />
          <input
            type="text"
            placeholder="Search moves..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-dark-700/50 border border-dark-600 rounded-lg text-white placeholder-dark-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-1">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-2 py-1 text-xs rounded transition-colors ${
                selectedCategory === category
                  ? 'bg-primary-600 text-white'
                  : 'bg-dark-700 text-dark-300 hover:bg-dark-600'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {/* AI Recommendations */}
        {aiRecommendations.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Zap className="w-4 h-4 text-yellow-400" />
              <h4 className="text-sm font-medium text-white">AI Recommendations</h4>
            </div>
            <div className="space-y-2">
              {aiRecommendations.map((move) => (
                <div
                  key={move.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, move.id)}
                  className="cursor-grab hover:bg-dark-700/30 transition-colors p-3 rounded-lg border border-yellow-600/30 bg-yellow-600/10 active:cursor-grabbing"
                >
                  <div className="flex items-start gap-3">
                    <span className="text-xl flex-shrink-0">{move.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h5 className="text-sm font-medium text-white truncate">{move.title}</h5>
                        {move.confidence && (
                          <Badge variant="outline" className="text-xs">
                            {move.confidence}/10
                          </Badge>
                        )}
                      </div>
                      
                      <p className="text-xs text-dark-300 mb-2 line-clamp-2">
                        {move.description}
                      </p>

                      <div className="space-y-1">
                        {move.monthlyDelta !== 0 && (
                          <div className="text-xs">
                            <span className="text-dark-400">Monthly: </span>
                            <span className={move.monthlyDelta > 0 ? 'text-red-400' : 'text-green-400'}>
                              {move.monthlyDelta > 0 ? '+' : ''}{formatCurrency(Math.abs(move.monthlyDelta))}
                            </span>
                          </div>
                        )}
                        {move.oneTime > 0 && (
                          <div className="text-xs">
                            <span className="text-dark-400">One-time: </span>
                            <span className="text-red-400">+{formatCurrency(move.oneTime)}</span>
                          </div>
                        )}
                        {move.cashInjection && (
                          <div className="text-xs">
                            <span className="text-dark-400">Cash: </span>
                            <span className="text-green-400">+{formatCurrency(move.cashInjection)}</span>
                          </div>
                        )}
                      </div>

                      <div className="flex flex-wrap gap-1 mt-2">
                        {move.badges.slice(0, 2).map((badge, index) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {badge}
                          </Badge>
                        ))}
                        {move.badges.length > 2 && (
                          <Badge variant="outline" className="text-xs">
                            +{move.badges.length - 2}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Regular Moves */}
        {regularMoves.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-white mb-3">Available Moves</h4>
            <div className="space-y-2">
              {regularMoves.map((move) => (
                <div
                  key={move.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, move.id)}
                  className="cursor-grab hover:bg-dark-700/50 transition-colors p-3 rounded-lg border border-dark-700 bg-dark-800/30 active:cursor-grabbing"
                >
                  <div className="flex items-start gap-3">
                    <span className="text-xl flex-shrink-0">{move.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h5 className="text-sm font-medium text-white truncate">{move.title}</h5>
                        {move.effort && (
                          <Badge 
                            variant={move.effort === 'high' ? 'destructive' : move.effort === 'medium' ? 'default' : 'secondary'}
                            className="text-xs"
                          >
                            {move.effort}
                          </Badge>
                        )}
                      </div>
                      
                      <p className="text-xs text-dark-300 mb-2 line-clamp-2">
                        {move.description}
                      </p>

                      <div className="space-y-1">
                        {move.monthlyDelta !== 0 && (
                          <div className="text-xs">
                            <span className="text-dark-400">Monthly: </span>
                            <span className={move.monthlyDelta > 0 ? 'text-red-400' : 'text-green-400'}>
                              {move.monthlyDelta > 0 ? '+' : ''}{formatCurrency(Math.abs(move.monthlyDelta))}
                            </span>
                          </div>
                        )}
                        {move.oneTime > 0 && (
                          <div className="text-xs">
                            <span className="text-dark-400">One-time: </span>
                            <span className="text-red-400">+{formatCurrency(move.oneTime)}</span>
                          </div>
                        )}
                        {move.cashInjection && (
                          <div className="text-xs">
                            <span className="text-dark-400">Cash: </span>
                            <span className="text-green-400">+{formatCurrency(move.cashInjection)}</span>
                          </div>
                        )}
                      </div>

                      <div className="flex flex-wrap gap-1 mt-2">
                        {move.badges.slice(0, 2).map((badge, index) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {badge}
                          </Badge>
                        ))}
                        {move.badges.length > 2 && (
                          <Badge variant="outline" className="text-xs">
                            +{move.badges.length - 2}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Custom Move Creator */}
        <div className="pt-4 border-t border-dark-700/50">
          <Button variant="outline" className="w-full" size="sm">
            <Plus className="w-4 h-4 mr-2" />
            Create Custom Move
          </Button>
        </div>
      </div>
    </div>
  );
};
