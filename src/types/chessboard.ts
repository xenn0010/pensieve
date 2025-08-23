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
}

export interface ChessboardBranch {
  id: string;
  name: string;
  nodes: ChessboardNode[];
  createdAt: Date;
  updatedAt: Date;
  description?: string;
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
}

export interface ChessboardBaseline {
  runway: number;
  monthlyBurn: number;
  cashOnHand: number;
  description: string;
}

export interface ChessboardState {
  baseline: ChessboardBaseline;
  branches: ChessboardBranch[];
  moveLibrary: ChessboardMove[];
  selectedBranch: string | null;
  selectedNode: string | null;
  lastUpdated: Date;
}

export interface ChessboardStore extends ChessboardState {
  // Actions
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
  updateBaseline: (baseline: Partial<ChessboardBaseline>) => void;
}
