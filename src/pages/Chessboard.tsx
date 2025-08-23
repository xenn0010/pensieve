import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { 
  RotateCcw, 
  Save, 
  X,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { useDemoStore } from '../lib/demo-store';
import { useToast } from '../hooks/use-toast';
import { MoveLibrary } from '../components/chessboard/MoveLibrary';
import { EnhancedChessboardGrid } from '../components/chessboard/EnhancedChessboardGrid';
import { InspectorDrawer } from '../components/chessboard/InspectorDrawer';
import { SignalsFeed } from '../components/chessboard/SignalsFeed';
import { HistoryPanel } from '../components/chessboard/HistoryPanel';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import type { ChessboardNode } from '../lib/demo-store';

const Chessboard: React.FC = () => {
  const { store, resetChessboard, savePlaybook } = useDemoStore();
  const { toast } = useToast();
  const [selectedNode, setSelectedNode] = useState<ChessboardNode | null>(null);
  const [inspectorOpen, setInspectorOpen] = useState(false);
  const [rightPanelOpen, setRightPanelOpen] = useState(false);

  const handleNodeClick = (node: ChessboardNode) => {
    setSelectedNode(node);
    setInspectorOpen(true);
  };

  const handleReset = () => {
    resetChessboard();
    toast({
      title: "Board Reset",
      description: "All moves cleared from all branches"
    });
  };

  const handleSave = () => {
    savePlaybook();
    const summary = store.chessboard.branches
      .map(b => {
        const finalNode = b.nodes[b.nodes.length - 1];
        const runway = finalNode ? finalNode.runway : store.chessboard.baseline.runway;
        return `${b.name} ${runway}m`;
      })
      .join(' • ');

    toast({
      title: "Playbook Saved",
      description: `Saved: ${summary}`,
      variant: "default"
    });
  };

  const formatCurrency = (amount: number): string => {
    if (amount >= 1000000) return `$${(amount / 1000000).toFixed(1)}M`;
    if (amount >= 1000) return `$${(amount / 1000).toFixed(0)}k`;
    return `$${amount.toFixed(0)}`;
  };

    return (
    <div className="min-h-screen bg-dark-900 text-white">
      {/* Header */}
      <div className="bg-dark-800/80 backdrop-blur-md border-b border-dark-700/50 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Scenario Chessboard</h1>
            <p className="text-dark-300 mt-1">
              Plan and visualize financial scenarios with AI-powered insights
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              onClick={() => setRightPanelOpen(!rightPanelOpen)}
              className="gap-2"
            >
              {rightPanelOpen ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
              {rightPanelOpen ? 'Hide' : 'Show'} Analysis
            </Button>

            <Button onClick={handleReset} variant="outline">
              <RotateCcw className="w-4 h-4 mr-2" />
              Reset
            </Button>

            <Button onClick={handleSave} variant="default">
              <Save className="w-4 h-4 mr-2" />
              Export Playbook
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex h-[calc(100vh-120px)]">
        {/* Left Panel - Enhanced Move Library */}
        <MoveLibrary />

        {/* Center - Enhanced Chessboard Grid */}
        <EnhancedChessboardGrid onNodeClick={handleNodeClick} />

        {/* Right Panel - Signals & Analysis (Collapsible) */}
        {rightPanelOpen && (
          <div className="w-80 bg-dark-800/60 backdrop-blur-md border-l border-dark-700/50 p-4">
            <div className="flex items-center justify-between mb-4">
              <CardTitle>AI Insights</CardTitle>
              <Button
                onClick={() => setRightPanelOpen(false)}
                variant="ghost"
                size="icon"
                className="h-6 w-6"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>

            <Tabs defaultValue="signals" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="signals">Signals</TabsTrigger>
                <TabsTrigger value="history">History</TabsTrigger>
              </TabsList>
              
              <TabsContent value="signals">
                <SignalsFeed />
              </TabsContent>
              
              <TabsContent value="history">
                <HistoryPanel />
              </TabsContent>
            </Tabs>
          </div>
        )}
      </div>

      {/* Inspector Drawer */}
      <InspectorDrawer
        node={selectedNode}
        isOpen={inspectorOpen}
        onClose={() => setInspectorOpen(false)}
      />
    </div>
  );
};

export default Chessboard;
