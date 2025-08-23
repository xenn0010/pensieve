import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { X, TrendingUp, TrendingDown, DollarSign, Clock, Target, Zap } from 'lucide-react';
import type { ChessboardNode } from '../../lib/demo-store';

interface InspectorDrawerProps {
  node: ChessboardNode | null;
  isOpen: boolean;
  onClose: () => void;
}

export const InspectorDrawer: React.FC<InspectorDrawerProps> = ({
  node,
  isOpen,
  onClose
}) => {
  if (!isOpen || !node) return null;

  const formatCurrency = (amount: number): string => {
    if (amount >= 1000000) return `$${(amount / 1000000).toFixed(1)}M`;
    if (amount >= 1000) return `$${(amount / 1000).toFixed(0)}k`;
    return `$${amount.toFixed(0)}`;
  };

  const getImpactColor = (delta: number) => {
    if (delta > 0) return 'text-red-400';
    if (delta < 0) return 'text-green-400';
    return 'text-gray-400';
  };

  const getConfidenceColor = (confidence?: number) => {
    if (!confidence) return 'text-gray-400';
    if (confidence >= 8) return 'text-green-400';
    if (confidence >= 6) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl max-h-[90vh] overflow-auto">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-3xl">{node.icon}</span>
              <div>
                <CardTitle>{node.title}</CardTitle>
                <div className="flex items-center gap-2 mt-1">
                  <Badge variant={node.isAiRecommended ? 'default' : 'secondary'}>
                    {node.isAiRecommended ? 'AI Recommended' : node.isCustom ? 'Custom' : 'Library'}
                  </Badge>
                  {node.confidence && (
                    <Badge variant="outline" className={getConfidenceColor(node.confidence)}>
                      {node.confidence}/10 Confidence
                    </Badge>
                  )}
                </div>
              </div>
            </div>
            <Button onClick={onClose} variant="ghost" size="icon">
              <X className="w-4 h-4" />
            </Button>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Description */}
          {node.description && (
            <div>
              <h4 className="text-sm font-medium text-white mb-2">Description</h4>
              <p className="text-sm text-dark-300 leading-relaxed">
                {node.description}
              </p>
            </div>
          )}

          {/* Financial Impact */}
          <div>
            <h4 className="text-sm font-medium text-white mb-3">Financial Impact</h4>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 bg-dark-800/50 rounded-lg border border-dark-700">
                <div className="flex items-center gap-2 mb-1">
                  <TrendingUp className="w-4 h-4 text-blue-400" />
                  <span className="text-xs text-dark-300">Monthly Impact</span>
                </div>
                <div className={`text-lg font-semibold ${getImpactColor(node.monthlyDelta)}`}>
                  {node.monthlyDelta > 0 ? '+' : ''}{formatCurrency(Math.abs(node.monthlyDelta))}
                </div>
                <div className="text-xs text-dark-400">
                  {node.monthlyDelta > 0 ? 'Increased costs' : 'Cost savings'}
                </div>
              </div>

              <div className="p-3 bg-dark-800/50 rounded-lg border border-dark-700">
                <div className="flex items-center gap-2 mb-1">
                  <DollarSign className="w-4 h-4 text-yellow-400" />
                  <span className="text-xs text-dark-300">One-time Cost</span>
                </div>
                <div className="text-lg font-semibold text-red-400">
                  {formatCurrency(node.oneTime)}
                </div>
                <div className="text-xs text-dark-400">Implementation cost</div>
              </div>

              {node.cashInjection && (
                <div className="p-3 bg-dark-800/50 rounded-lg border border-dark-700 col-span-2">
                  <div className="flex items-center gap-2 mb-1">
                    <TrendingUp className="w-4 h-4 text-green-400" />
                    <span className="text-xs text-dark-300">Cash Injection</span>
                  </div>
                  <div className="text-lg font-semibold text-green-400">
                    +{formatCurrency(node.cashInjection)}
                  </div>
                  <div className="text-xs text-dark-400">Capital raised</div>
                </div>
              )}
            </div>
          </div>

          {/* Runway Impact */}
          <div>
            <h4 className="text-sm font-medium text-white mb-3">Runway Impact</h4>
            <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-dark-300">New Runway</span>
                <span className="text-lg font-semibold text-white">{node.runway} months</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-dark-300">Monthly Burn</span>
                <span className="text-lg font-semibold text-white">{formatCurrency(node.monthlyBurn)}</span>
              </div>
            </div>
          </div>

          {/* Impact Analysis */}
          {node.impact && (
            <div>
              <h4 className="text-sm font-medium text-white mb-2">Expected Impact</h4>
              <p className="text-sm text-dark-300 leading-relaxed">
                {node.impact}
              </p>
            </div>
          )}

          {/* Categories & Tags */}
          <div>
            <h4 className="text-sm font-medium text-white mb-3">Categories & Tags</h4>
            <div className="flex flex-wrap gap-2">
              {node.category && (
                <Badge variant="default">{node.category}</Badge>
              )}
              {node.badges.map((badge, index) => (
                <Badge key={index} variant="secondary">
                  {badge}
                </Badge>
              ))}
            </div>
          </div>

          {/* Metadata */}
          <div>
            <h4 className="text-sm font-medium text-white mb-3">Metadata</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-dark-400">Source:</span>
                <span className="text-white ml-2">{node.source || 'Unknown'}</span>
              </div>
              <div>
                <span className="text-dark-400">Created:</span>
                <span className="text-white ml-2">
                  {node.createdAt.toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>

          {/* Sensitivity Analysis */}
          {node.sensitivity && (
            <div>
              <h4 className="text-sm font-medium text-white mb-3">Sensitivity Analysis</h4>
              <div className="space-y-2">
                {node.sensitivity.fx && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-dark-300">FX Impact:</span>
                    <span className="text-white">{node.sensitivity.fx}% variance</span>
                  </div>
                )}
                {node.sensitivity.cac && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-dark-300">CAC Impact:</span>
                    <span className="text-white">{node.sensitivity.cac}% variance</span>
                  </div>
                )}
                {node.sensitivity.churn && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-dark-300">Churn Impact:</span>
                    <span className="text-white">{node.sensitivity.churn}% variance</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center gap-2 pt-4 border-t border-dark-700">
            <Button variant="outline" size="sm">
              <Zap className="w-4 h-4 mr-2" />
              Resimulate
            </Button>
            <Button variant="outline" size="sm">
              <Target className="w-4 h-4 mr-2" />
              Set Target
            </Button>
            <Button variant="destructive" size="sm">
              Remove Move
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
