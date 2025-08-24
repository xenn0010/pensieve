export const API_CONFIG = {
  BASE_URL: 'http://localhost:8001',
  ENDPOINTS: {
    // Health & Status
    HEALTH: '/health',
    
    // Dashboard
    DASHBOARD_OVERVIEW: '/dashboard/overview',
    DASHBOARD_METRICS: '/dashboard/metrics',
    
    // Financial Data
    FINANCIAL_KPIS: '/financial/kpis',
    FINANCIAL_TRANSACTIONS: '/financial/transactions',
    FINANCIAL_SCENARIOS: '/financial/scenarios',
    FINANCIAL_SCENARIO_SWITCH: '/financial/scenario',
    
    // Company Research
    COMPANY_RESEARCH: '/research/company',
    
    // Agent & Intelligence
    AGENT_QUERY: '/agent/query',
    INTELLIGENCE_SIGNALS: '/intelligence/signals',
    
    // Actions
    ACTIONS_RECENT: '/actions/recent',
    ACTIONS_PERFORMANCE: '/actions/performance',
    
    // Real-time
    REALTIME_STATUS: '/realtime/status'
  },
  
  // WebSocket URLs
  WEBSOCKETS: {
    FINANCIAL: 'ws://localhost:8001/ws/financial'
  }
};

// Helper function to build full API URLs
export const buildApiUrl = (endpoint: string, params?: Record<string, string>): string => {
  let url = `${API_CONFIG.BASE_URL}${endpoint}`;
  
  if (params) {
    const searchParams = new URLSearchParams(params);
    url += `?${searchParams.toString()}`;
  }
  
  return url;
};

// Helper function to build WebSocket URLs
export const buildWebSocketUrl = (type: keyof typeof API_CONFIG.WEBSOCKETS): string => {
  return API_CONFIG.WEBSOCKETS[type];
};
