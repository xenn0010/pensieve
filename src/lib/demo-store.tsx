import { create } from 'zustand';

// Types
export interface ChessboardNode {
  id: string;
  title: string;
  icon: string;
  monthlyDelta: number;
  oneTime: number;
  cashInjection?: number;
  runway: number;
  monthlyBurn: number;
  badges: string[];
  isAiRecommended: boolean;
  isCustom: boolean;
  createdAt: Date;
  description?: string;
  impact?: string;
  source?: string;
  category?: string;
  confidence?: number;
  sensitivity?: {
    fx?: number;
    cac?: number;
    churn?: number;
  };
}

export interface ChessboardBranch {
  id: string;
  name: string;
  nodes: ChessboardNode[];
  createdAt: Date;
  updatedAt: Date;
  description?: string;
  color?: string;
  isActive?: boolean;
}

export interface ChessboardMove {
  id: string;
  title: string;
  icon: string;
  monthlyDelta: number;
  oneTime: number;
  cashInjection?: number;
  badges: string[];
  category: string;
  description: string;
  impact: string;
  source: string;
  isAiRecommended: boolean;
  isCustom: boolean;
  createdAt: Date;
  confidence?: number;
  effort?: 'low' | 'medium' | 'high';
  timeline?: string;
}

export interface Signal {
  id: string;
  type: 'positive' | 'negative' | 'neutral';
  category: 'financial' | 'competitive' | 'market' | 'regulatory' | 'operational';
  title: string;
  description: string;
  severity: number;
  timestamp: Date;
  source: string;
  impact: string;
  companyName?: string;
  relevance?: number;
}

interface DemoStore {
  chessboard: {
    baseline: {
      runway: number;
      monthlyBurn: number;
      cashOnHand: number;
      description: string;
    };
    branches: ChessboardBranch[];
    moveLibrary: ChessboardMove[];
    selectedBranch: string | null;
    selectedNode: string | null;
    lastUpdated: Date;
    signals: Signal[];
    history: Array<{
      id: string;
      action: string;
      timestamp: Date;
      data: any;
    }>;
  };
  addChessboardMove: (branchId: string, moveId: string) => void;
  removeBranchMove: (branchId: string) => void;
  addBranch: () => void;
  removeBranch: (branchId: string) => void;
  duplicateBranch: (branchId: string) => void;
  resetChessboard: () => void;
  savePlaybook: () => void;
  addCustomMove: (moveData: Omit<ChessboardMove, 'id' | 'createdAt'>) => void;
  selectBranch: (branchId: string | null) => void;
  selectNode: (nodeId: string | null) => void;
  updateBaseline: (baseline: any) => void;
  addSignal: (signal: Omit<Signal, 'id' | 'timestamp'>) => void;
  getAiRecommendations: () => ChessboardMove[];
}

// Initial data
const initialBaseline = {
  runway: 18.5,
  monthlyBurn: 130000,
  cashOnHand: 2400000,
  description: 'Current financial state'
};

const initialMoveLibrary: ChessboardMove[] = [
  {
    id: 'hire_devs',
    title: 'Hire 3 Senior Developers',
    icon: '👨‍💻',
    monthlyDelta: 45000,
    oneTime: 15000,
    badges: ['Growth', 'Team', 'Investment'],
    category: 'Hiring',
    description: 'Expand engineering team for product development',
    impact: 'Increased development capacity and feature velocity',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date(),
    confidence: 8,
    effort: 'medium',
    timeline: '2-3 months'
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
    impact: 'Immediate cost savings, potential growth impact',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date(),
    confidence: 9,
    effort: 'low',
    timeline: '1 month'
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
    impact: 'Significant cash injection for growth',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date(),
    confidence: 6,
    effort: 'high',
    timeline: '6-9 months'
  },
  {
    id: 'automation_tools',
    title: 'Automation & AI Tools',
    icon: '⚡',
    monthlyDelta: 5000,
    oneTime: 25000,
    badges: ['Efficiency', 'Technology'],
    category: 'Technology',
    description: 'Invest in automation and AI productivity tools',
    impact: 'Improved team efficiency and reduced manual work',
    source: 'Library',
    isAiRecommended: true,
    isCustom: false,
    createdAt: new Date(),
    confidence: 7,
    effort: 'medium',
    timeline: '2-4 months'
  },
  {
    id: 'enterprise_sales',
    title: 'Enterprise Sales Team',
    icon: '🎯',
    monthlyDelta: 35000,
    oneTime: 20000,
    badges: ['Revenue', 'Sales', 'Growth'],
    category: 'Sales',
    description: 'Build dedicated enterprise sales team',
    impact: 'Higher ACV deals and enterprise market penetration',
    source: 'Library',
    isAiRecommended: true,
    isCustom: false,
    createdAt: new Date(),
    confidence: 7,
    effort: 'high',
    timeline: '3-6 months'
  },
  {
    id: 'office_downsize',
    title: 'Office Space Optimization',
    icon: '🏢',
    monthlyDelta: -12000,
    oneTime: 8000,
    badges: ['Cost Reduction', 'Remote'],
    category: 'Facilities',
    description: 'Downsize office space for hybrid work model',
    impact: 'Reduced real estate costs, improved work flexibility',
    source: 'Library',
    isAiRecommended: false,
    isCustom: false,
    createdAt: new Date(),
    confidence: 8,
    effort: 'medium',
    timeline: '2-3 months'
  }
];

const initialSignals: Signal[] = [
  {
    id: 's1',
    type: 'positive',
    category: 'competitive',
    title: 'Competitor raises $10M Series A',
    description: 'Main competitor TechFlow secured $10M Series A, indicating market validation',
    severity: 3,
    timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    source: 'TechCrunch',
    impact: 'Market validation for our sector',
    companyName: 'TechFlow',
    relevance: 8
  },
  {
    id: 's2',
    type: 'negative',
    category: 'market',
    title: 'Economic uncertainty rising',
    description: 'Federal Reserve signals potential interest rate increases',
    severity: 4,
    timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    source: 'Fed Minutes',
    impact: 'Fundraising may become more challenging',
    relevance: 7
  },
  {
    id: 's3',
    type: 'positive',
    category: 'market',
    title: 'Industry growth accelerating',
    description: 'SaaS market projected to grow 25% this year',
    severity: 3,
    timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    source: 'Gartner Report',
    impact: 'Favorable market conditions for growth',
    relevance: 9
  }
];

// Helper functions
const calculateRunway = (monthlyBurn: number, cashOnHand: number): number => {
  if (monthlyBurn <= 0) return Infinity;
  return Math.round((cashOnHand / monthlyBurn) * 10) / 10;
};

const createNodeFromMove = (move: ChessboardMove, previousNode?: ChessboardNode, baseline?: any): ChessboardNode => {
  const prevBurn = previousNode ? previousNode.monthlyBurn : (baseline?.monthlyBurn || initialBaseline.monthlyBurn);
  const newMonthlyBurn = prevBurn + move.monthlyDelta;
  const cashAdded = (move.cashInjection || 0) - move.oneTime;
  const newCashOnHand = (baseline?.cashOnHand || initialBaseline.cashOnHand) + cashAdded;
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
    source: move.source,
    category: move.category,
    confidence: move.confidence
  };
};

export const useDemoStore = create<{ store: DemoStore } & DemoStore>((set, get) => ({
  store: {
    chessboard: {
      baseline: initialBaseline,
      branches: [],
      moveLibrary: initialMoveLibrary,
      selectedBranch: null,
      selectedNode: null,
      lastUpdated: new Date(),
      signals: initialSignals,
      history: []
    }
  } as any,

  addChessboardMove: (branchId: string, moveId: string) => {
    const { store } = get();
    const move = store.chessboard.moveLibrary.find(m => m.id === moveId);
    const branch = store.chessboard.branches.find(b => b.id === branchId);
    
    if (!move || !branch) return;

    const lastNode = branch.nodes[branch.nodes.length - 1];
    const newNode = createNodeFromMove(move, lastNode, store.chessboard.baseline);
    
    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          branches: state.store.chessboard.branches.map(b => 
            b.id === branchId 
              ? { ...b, nodes: [...b.nodes, newNode], updatedAt: new Date() }
              : b
          ),
          lastUpdated: new Date(),
          history: [...state.store.chessboard.history, {
            id: `h_${Date.now()}`,
            action: `Added ${move.title} to ${branch.name}`,
            timestamp: new Date(),
            data: { branchId, moveId, nodeId: newNode.id }
          }]
        }
      }
    }));
  },

  removeBranchMove: (branchId: string) => {
    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          branches: state.store.chessboard.branches.map(b => 
            b.id === branchId 
              ? { ...b, nodes: b.nodes.slice(0, -1), updatedAt: new Date() }
              : b
          ),
          lastUpdated: new Date()
        }
      }
    }));
  },

  addBranch: () => {
    const { store } = get();
    const newBranch: ChessboardBranch = {
      id: `branch_${Date.now()}`,
      name: `Scenario ${store.chessboard.branches.length + 1}`,
      nodes: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      description: 'New scenario branch',
      color: `hsl(${Math.random() * 360}, 70%, 50%)`,
      isActive: true
    };

    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          branches: [...state.store.chessboard.branches, newBranch],
          lastUpdated: new Date()
        }
      }
    }));
  },

  removeBranch: (branchId: string) => {
    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          branches: state.store.chessboard.branches.filter(b => b.id !== branchId),
          selectedBranch: state.store.chessboard.selectedBranch === branchId ? null : state.store.chessboard.selectedBranch,
          lastUpdated: new Date()
        }
      }
    }));
  },

  duplicateBranch: (branchId: string) => {
    const { store } = get();
    const originalBranch = store.chessboard.branches.find(b => b.id === branchId);
    
    if (!originalBranch) return;

    const newBranch: ChessboardBranch = {
      ...originalBranch,
      id: `branch_${Date.now()}`,
      name: `${originalBranch.name} (Copy)`,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          branches: [...state.store.chessboard.branches, newBranch],
          lastUpdated: new Date()
        }
      }
    }));
  },

  resetChessboard: () => {
    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          branches: [],
          selectedBranch: null,
          selectedNode: null,
          lastUpdated: new Date()
        }
      }
    }));
  },

  savePlaybook: () => {
    const { store } = get();
    console.log('Playbook saved:', store.chessboard.branches);
    
    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          lastUpdated: new Date()
        }
      }
    }));
  },

  addCustomMove: (moveData) => {
    const newMove: ChessboardMove = {
      ...moveData,
      id: `custom_${Date.now()}`,
      createdAt: new Date(),
      isCustom: true
    };

    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          moveLibrary: [...state.store.chessboard.moveLibrary, newMove],
          lastUpdated: new Date()
        }
      }
    }));
  },

  selectBranch: (branchId: string | null) => {
    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          selectedBranch: branchId
        }
      }
    }));
  },

  selectNode: (nodeId: string | null) => {
    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          selectedNode: nodeId
        }
      }
    }));
  },

  updateBaseline: (baselineUpdates) => {
    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          baseline: { ...state.store.chessboard.baseline, ...baselineUpdates },
          lastUpdated: new Date()
        }
      }
    }));
  },

  addSignal: (signalData) => {
    const newSignal: Signal = {
      ...signalData,
      id: `signal_${Date.now()}`,
      timestamp: new Date()
    };

    set((state) => ({
      store: {
        ...state.store,
        chessboard: {
          ...state.store.chessboard,
          signals: [newSignal, ...state.store.chessboard.signals],
          lastUpdated: new Date()
        }
      }
    }));
  },

  getAiRecommendations: () => {
    const { store } = get();
    return store.chessboard.moveLibrary.filter(move => move.isAiRecommended);
  }
}));
