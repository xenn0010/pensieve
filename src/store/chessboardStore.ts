import { create } from 'zustand';
import { ChessboardStore, ChessboardBaseline, ChessboardBranch, ChessboardMove, ChessboardNode } from '../types/chessboard';

// Initial baseline data
const initialBaseline: ChessboardBaseline = {
  runway: 18.5,
  monthlyBurn: 130000,
  cashOnHand: 2400000,
  description: 'Current financial state'
};

// Initial move library with common financial moves
const initialMoveLibrary: ChessboardMove[] = [
  {
    id: 'hire_devs',
    title: 'Hire 3 Developers',
    icon: '👨‍💻',
    monthlyDelta: 45000,
    oneTime: 15000,
    badges: ['Growth', 'Team', 'Investment'],
    category: 'Hiring',
    description: 'Expand engineering team for product development',
    impact: 'Increased development capacity',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date()
  },
  {
    id: 'cut_marketing',
    title: 'Reduce Marketing Spend',
    icon: '📉',
    monthlyDelta: -30000,
    oneTime: 0,
    badges: ['Cost Reduction', 'Efficiency'],
    category: 'Cost Control',
    description: 'Cut marketing budget by 40%',
    impact: 'Immediate cost savings',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date()
  },
  {
    id: 'raise_series_a',
    title: 'Raise Series A',
    icon: '💰',
    monthlyDelta: 25000,
    oneTime: 100000,
    cashInjection: 5000000,
    badges: ['Funding', 'Growth', 'Investment'],
    category: 'Fundraising',
    description: 'Raise $5M Series A funding round',
    impact: 'Significant cash injection',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date()
  },
  {
    id: 'office_expansion',
    title: 'Office Expansion',
    icon: '🏢',
    monthlyDelta: 8000,
    oneTime: 50000,
    badges: ['Growth', 'Infrastructure'],
    category: 'Facilities',
    description: 'Expand office space for growing team',
    impact: 'Better work environment',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date()
  },
  {
    id: 'automation_tools',
    title: 'Automation Tools',
    icon: '⚡',
    monthlyDelta: 5000,
    oneTime: 25000,
    badges: ['Efficiency', 'Technology'],
    category: 'Technology',
    description: 'Invest in automation and productivity tools',
    impact: 'Improved team efficiency',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date()
  }
];

// Helper function to calculate runway
const calculateRunway = (monthlyBurn: number, cashOnHand: number): number => {
  if (monthlyBurn <= 0) return Infinity;
  return Math.round((cashOnHand / monthlyBurn) * 10) / 10;
};

// Helper function to create a new node from a move
const createNodeFromMove = (move: ChessboardMove, previousNode?: ChessboardNode): ChessboardNode => {
  const previousBurn = previousNode ? previousNode.monthlyBurn : initialBaseline.monthlyBurn;
  
  const newMonthlyBurn = previousBurn + move.monthlyDelta;
  const newCashOnHand = (previousNode ? 0 : initialBaseline.cashOnHand) + (move.cashInjection || 0) - move.oneTime;
  const newRunway = calculateRunway(newMonthlyBurn, newCashOnHand);

  return {
    id: `${move.id}_${Date.now()}`,
    title: move.title,
    icon: move.icon,
    monthlyDelta: move.monthlyDelta,
    oneTime: move.oneTime,
    cashInjection: move.cashInjection,
    runway: newRunway,
    monthlyBurn: newMonthlyBurn,
    badges: move.badges,
    isAiRecommended: move.isAiRecommended,
    isCustom: move.isCustom,
    createdAt: new Date(),
    description: move.description,
    impact: move.impact,
    source: move.source
  };
};

export const useChessboardStore = create<ChessboardStore>((set, get) => ({
  // Initial state
  baseline: initialBaseline,
  branches: [],
  moveLibrary: initialMoveLibrary,
  selectedBranch: null,
  selectedNode: null,
  lastUpdated: new Date(),

  // Actions
  addChessboardMove: (branchId: string, moveId: string) => {
    const { branches, moveLibrary } = get();
    const move = moveLibrary.find(m => m.id === moveId);
    const branch = branches.find(b => b.id === branchId);
    
    if (!move || !branch) return;

    const lastNode = branch.nodes[branch.nodes.length - 1];
    const newNode = createNodeFromMove(move, lastNode);
    
    set((state) => ({
      branches: state.branches.map(b => 
        b.id === branchId 
          ? { ...b, nodes: [...b.nodes, newNode], updatedAt: new Date() }
          : b
      ),
      lastUpdated: new Date()
    }));
  },

  removeBranchMove: (branchId: string) => {
    set((state) => ({
      branches: state.branches.map(b => 
        b.id === branchId 
          ? { ...b, nodes: b.nodes.slice(0, -1), updatedAt: new Date() }
          : b
      ),
      lastUpdated: new Date()
    }));
  },

  addBranch: () => {
    const newBranch: ChessboardBranch = {
      id: `branch_${Date.now()}`,
      name: `Scenario ${get().branches.length + 1}`,
      nodes: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      description: 'New scenario branch'
    };

    set((state) => ({
      branches: [...state.branches, newBranch],
      lastUpdated: new Date()
    }));
  },

  removeBranch: (branchId: string) => {
    set((state) => ({
      branches: state.branches.filter(b => b.id !== branchId),
      selectedBranch: state.selectedBranch === branchId ? null : state.selectedBranch,
      lastUpdated: new Date()
    }));
  },

  duplicateBranch: (branchId: string) => {
    const { branches } = get();
    const originalBranch = branches.find(b => b.id === branchId);
    
    if (!originalBranch) return;

    const newBranch: ChessboardBranch = {
      ...originalBranch,
      id: `branch_${Date.now()}`,
      name: `${originalBranch.name} (Copy)`,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    set((state) => ({
      branches: [...state.branches, newBranch],
      lastUpdated: new Date()
    }));
  },

  resetChessboard: () => {
    set({
      branches: [],
      selectedBranch: null,
      selectedNode: null,
      lastUpdated: new Date()
    });
  },

  savePlaybook: () => {
    // In a real app, this would save to backend/localStorage
    console.log('Playbook saved:', get().branches);
    set({ lastUpdated: new Date() });
  },

  addCustomMove: (moveData) => {
    const newMove: ChessboardMove = {
      ...moveData,
      id: `custom_${Date.now()}`,
      createdAt: new Date()
    };

    set((state) => ({
      moveLibrary: [...state.moveLibrary, newMove],
      lastUpdated: new Date()
    }));
  },

  selectBranch: (branchId: string | null) => {
    set({ selectedBranch: branchId });
  },

  selectNode: (nodeId: string | null) => {
    set({ selectedNode: nodeId });
  },

  updateBaseline: (baselineUpdates) => {
    set((state) => ({
      baseline: { ...state.baseline, ...baselineUpdates },
      lastUpdated: new Date()
    }));
  }
}));
