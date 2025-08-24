export interface FinancialTransaction {
  id: string;
  type: 'expense' | 'revenue' | 'transfer' | 'payroll' | 'vendor';
  amount: number;
  currency: string;
  description: string;
  category: string;
  timestamp: string;
  status: 'pending' | 'completed' | 'failed';
  merchant: string;
}

export interface FinancialKPIs {
  runway_months: number;
  cash_on_hand: number;
  monthly_burn: number;
  scenario: string;
  last_updated: string;
  trends: {
    runway_change: number;
    cash_change: number;
    burn_change: number;
  };
}

export interface FinancialSummary {
  total_revenue: number;
  total_expenses: number;
  net_cash_flow: number;
  transaction_count: number;
}

export interface FinancialScenario {
  id: string;
  name: string;
  description: string;
  runway_months: number;
  cash_on_hand: number;
  monthly_burn: number;
  status: 'active' | 'available';
}

export interface FinancialDataResponse {
  transactions: FinancialTransaction[];
  summary: FinancialSummary;
}
