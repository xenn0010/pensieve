import { create } from 'zustand';
import { Company } from '../types/company';

interface GodmodeState {
  isActive: boolean;
  selectedCompany: Company | null;
  globeConfig: {
    backgroundColor: string;
    pointSize: number;
    animationSpeed: number;
    autoRotate: boolean;
  };
  // Actions
  toggleGodmode: () => void;
  setSelectedCompany: (company: Company | null) => void;
  updateGlobeConfig: (config: Partial<GodmodeState['globeConfig']>) => void;
  resetGlobe: () => void;
}

export const useGodmodeStore = create<GodmodeState>((set, get) => ({
  isActive: false,
  selectedCompany: null,
  globeConfig: {
    backgroundColor: '#0f172a', // dark-900
    pointSize: 8,
    animationSpeed: 1,
    autoRotate: true,
  },

  toggleGodmode: () => {
    const { isActive } = get();
    set({ 
      isActive: !isActive,
      selectedCompany: null // Reset selection when toggling
    });
  },

  setSelectedCompany: (company) => {
    set({ selectedCompany: company });
  },

  updateGlobeConfig: (config) => {
    set((state) => ({
      globeConfig: { ...state.globeConfig, ...config }
    }));
  },

  resetGlobe: () => {
    set({
      selectedCompany: null,
      globeConfig: {
        backgroundColor: '#0f172a',
        pointSize: 8,
        animationSpeed: 1,
        autoRotate: true,
      }
    });
  },
}));
