import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Plus, 
  Trash2, 
  Copy, 
  ChevronDown, 
  ChevronRight, 
  BarChart3, 
  Table2, 
  Eye,
  Play,
  X,
  Zap
} from 'lucide-react';
import { useDemoStore } from '../../lib/demo-store';
import { useToast } from '../../hooks/use-toast';
import type { ChessboardNode, ChessboardBranch } from '../../lib/demo-store';
import { EnhancedCompareTable } from '../ui/enhanced-compare-table';
import { VisualCompareChart } from './VisualCompareChart';

interface EnhancedChessboardGridProps {
  onNodeClick: (node: ChessboardNode) => void;
}

export const EnhancedChessboardGrid: React.FC<EnhancedChessboardGridProps> = ({ onNodeClick }) => {
  const { 
    store, 
    addChessboardMove, 
    removeBranchMove, 
    addBranch, 
    removeBranch, 
    duplicateBranch 
  } = useDemoStore();
  const { toast } = useToast();
  const [draggedMove, setDraggedMove] = useState<string | null>(null);
  const [collapsedBranches, setCollapsedBranches] = useState<Set<string>>(new Set());
  const [compareMode, setCompareMode] = useState(false);
  const [visualMode, setVisualMode] = useState(false);

  const formatCurrency = (amount: number): string => {
    if (amount >= 1000000) return `$${(amount / 1000000).toFixed(1)}M`;
    if (amount >= 1000) return `$${(amount / 1000).toFixed(0)}k`;
    return `$${amount.toFixed(0)}`;
  };

  const formatNumber = (num: number): string => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(0)}k`;
    return num.toString();
  };

  const getRunwayRange = (nodes: ChessboardNode[]): string => {
    if (nodes.length === 0) return `${store.chessboard.baseline.runway}m`;
    const runways = nodes.map(n => n.runway);
    const min = Math.min(...runways);
    const max = Math.max(...runways);
    return min === max ? `${min}m` : `${min}-${max}m`;
  };

  const getProvenance = (node: ChessboardNode): string => {
    if (node.isAiRecommended) return "AI";
    if (node.isCustom) return "Custom";
    return "Library";
  };

  const getBadgeVariant = (badge: string): "default" | "secondary" | "outline" => {
    const positiveWords = ['growth', 'expansion', 'revenue', 'efficiency', 'scale'];
    const negativeWords = ['reduction', 'cut', 'layoff', 'cost', 'expense'];

    if (positiveWords.some(word => badge.toLowerCase().includes(word))) return "default";
    if (negativeWords.some(word => badge.toLowerCase().includes(word))) return "outline";
    return "secondary";
  };

  const handleDragOver = (e: React.DragEvent, branchId: string) => {
    e.preventDefault();
    e.currentTarget.classList.add('bg-primary/10', 'border-primary/50');
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.currentTarget.classList.remove('bg-primary/10', 'border-primary/50');
  };

  const handleDrop = (e: React.DragEvent, branchId: string) => {
    e.preventDefault();
    e.currentTarget.classList.remove('bg-primary/10', 'border-primary/50');

    const moveId = e.dataTransfer.getData('text/plain');
    if (moveId) {
      addChessboardMove(branchId, moveId);
      const move = store.chessboard.moveLibrary.find(m => m.id === moveId);
      toast({
        title: "Move Added",
        description: `${move?.title} added to scenario`,
        variant: "default"
      });
    }
  };

  const handleRemoveNode = (branchId: string) => {
    removeBranchMove(branchId);
    toast({
      title: "Move Removed",
      description: `Last move removed from scenario`,
      variant: "default"
    });
  };

  const handleDuplicateBranch = (branchId: string) => {
    duplicateBranch(branchId);
    toast({
      title: "Scenario Duplicated",
      description: `Created copy of scenario`,
      variant: "default"
    });
  };

  const handleResimulate = (branchId: string) => {
    toast({
      title: "Resimulating",
      description: `Recalculating scenario projections`,
      variant: "default"
    });
  };

  const toggleBranchCollapse = (branchId: string) => {
    const newCollapsed = new Set(collapsedBranches);
    if (newCollapsed.has(branchId)) {
      newCollapsed.delete(branchId);
    } else {
      newCollapsed.add(branchId);
    }
    setCollapsedBranches(newCollapsed);
  };

  const handleAddBranch = () => {
    addBranch();
    toast({
      title: "Scenario Created",
      description: "New scenario branch ready for planning",
      variant: "default"
    });
  };

  if (compareMode && !visualMode) {
    return (
      <EnhancedCompareTable
        baseline={{
          cash: store.chessboard.baseline.cashOnHand,
          burn: store.chessboard.baseline.monthlyBurn,
          runway: store.chessboard.baseline.runway
        }}
        branches={store.chessboard.branches}
        onClose={() => setCompareMode(false)}
      />
    );
  }

  if (visualMode) {
    return (
      <VisualCompareChart
        baseline={{
          cash: store.chessboard.baseline.cashOnHand,
          burn: store.chessboard.baseline.monthlyBurn,
          runway: store.chessboard.baseline.runway
        }}
        branches={store.chessboard.branches}
        onClose={() => setVisualMode(false)}
      />
    );
  }

  return (
    <div className="flex-1 p-6 overflow-auto">
      <div className="max-w-6xl mx-auto">
        {/* Controls */}
        <div className="flex items-center gap-3 mb-6">
          <Button onClick={handleAddBranch} className="gap-2">
            <Plus className="w-4 h-4" />
            Add Scenario
          </Button>
          
          <Button
            onClick={() => setCompareMode(true)}
            variant="outline"
            className="gap-2"
          >
            <Table2 className="w-4 h-4" />
            Compare Table
          </Button>
          
          <Button
            onClick={() => setVisualMode(true)}
            variant="outline"
            className="gap-2"
          >
            <BarChart3 className="w-4 h-4" />
            Visual Compare
          </Button>
        </div>



        {/* Scenario Branches */}
        {store.chessboard.branches.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <div className="text-6xl mb-4">♟️</div>
              <h3 className="text-xl font-semibold mb-2">No Scenarios Yet</h3>
              <p className="text-dark-300 mb-6">
                Create your first financial scenario to start planning
              </p>
              <Button onClick={handleAddBranch} size="lg">
                Create First Scenario
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {store.chessboard.branches.map((branch) => {
              const isCollapsed = collapsedBranches.has(branch.id);
              const finalNode = branch.nodes.length > 0 ? branch.nodes[branch.nodes.length - 1] : null;
              const finalRunway = finalNode ? finalNode.runway : store.chessboard.baseline.runway;
              const runwayDelta = finalNode ? finalRunway - store.chessboard.baseline.runway : 0;

              return (
                <Card key={branch.id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <Button
                          onClick={() => toggleBranchCollapse(branch.id)}
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6"
                        >
                          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </Button>
                        
                        <CardTitle>{branch.name}</CardTitle>
                        
                        <Badge variant="outline">
                          {branch.nodes.length} move{branch.nodes.length !== 1 ? 's' : ''}
                        </Badge>
                        
                        <Badge variant={runwayDelta > 0 ? 'default' : 'destructive'}>
                          Final: {finalRunway}m
                          {runwayDelta !== 0 && (
                            <span className={runwayDelta > 0 ? 'text-green-400' : 'text-red-400'}>
                              ({runwayDelta > 0 ? '+' : ''}{runwayDelta}m)
                            </span>
                          )}
                        </Badge>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <Button
                          onClick={() => handleDuplicateBranch(branch.id)}
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6"
                        >
                          <Copy className="w-4 h-4" />
                        </Button>
                        <Button
                          onClick={() => removeBranch(branch.id)}
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6 text-red-400 hover:text-red-300"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  
                  {!isCollapsed && (
                    <CardContent>
                      {/* Nodes */}
                      {branch.nodes.length > 0 && (
                        <div className="space-y-3 mb-6">
                          {branch.nodes.map((node, index) => (
                            <div
                              key={node.id}
                              onClick={() => onNodeClick(node)}
                              className="flex items-center gap-3 p-3 rounded-lg border border-dark-700 bg-dark-800/50 hover:bg-dark-700/50 cursor-pointer transition-colors"
                            >
                              <span className="text-2xl">{node.icon}</span>
                              
                              <div className="flex-1">
                                <div className="flex items-center gap-2 mb-1">
                                  <h4 className="font-medium text-white">{node.title}</h4>
                                  <Badge variant="outline" className="text-xs">
                                    {getProvenance(node)}
                                  </Badge>
                                </div>
                                
                                <div className="text-sm text-dark-300">
                                  Step {index + 1} • Runway: {node.runway}m • Burn: {formatCurrency(node.monthlyBurn)}
                                </div>
                              </div>
                              
                              <div className="text-right">
                                {node.badges.slice(0, 2).map((badge, i) => (
                                  <Badge key={i} variant={getBadgeVariant(badge)} className="text-xs mr-1">
                                    {badge}
                                  </Badge>
                                ))}
                                {node.badges.length > 2 && (
                                  <Badge variant="outline" className="text-xs">
                                    +{node.badges.length - 2}
                                  </Badge>
                                )}
                              </div>
                              
                              <Button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleRemoveNode(branch.id);
                                }}
                                variant="ghost"
                                size="icon"
                                className="h-6 w-6 opacity-50 hover:opacity-100"
                              >
                                <X className="w-4 h-4" />
                              </Button>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Drop Zone */}
                      <div
                        onDragOver={(e) => handleDragOver(e, branch.id)}
                        onDragLeave={handleDragLeave}
                        onDrop={(e) => handleDrop(e, branch.id)}
                        className="border-2 border-dashed border-dark-600/50 rounded-lg p-6 text-center text-dark-400 hover:border-primary-500/50 hover:bg-primary-500/5 transition-colors"
                      >
                        <div className="text-4xl mb-2">⬇️</div>
                        <p className="font-medium">Drag moves here to add to scenario</p>
                        
                        {branch.nodes.length === 0 && (
                          <p className="text-sm mt-2 text-dark-500">
                            This scenario starts from baseline
                          </p>
                        )}
                      </div>

                      {/* Branch Actions */}
                      <div className="flex items-center justify-between mt-4 pt-4 border-t border-dark-700/50">
                        <div className="text-sm text-dark-400">
                          Range: {getRunwayRange(branch.nodes)}
                        </div>
                        
                        <div className="flex items-center gap-2">
                          <Button
                            onClick={() => handleResimulate(branch.id)}
                            variant="outline"
                            size="sm"
                            className="h-6 px-2 text-xs gap-1"
                          >
                            <Zap className="w-3 h-3" />
                            Resimulate
                          </Button>
                          
                          {branch.nodes.length > 0 && (
                            <Button
                              onClick={() => handleRemoveNode(branch.id)}
                              variant="outline"
                              size="sm"
                              className="h-6 px-2 text-xs gap-1"
                            >
                              <X className="w-3 h-3" />
                              Undo Last
                            </Button>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  )}
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
