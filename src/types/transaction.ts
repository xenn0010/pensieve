export interface Transaction {
  id: string;
  companyId: string;
  companyName: string;
  type: 'investment' | 'acquisition' | 'partnership' | 'funding' | 'ipo' | 'merger';
  amount?: number;
  currency?: string;
  description: string;
  timestamp: Date;
  status: 'pending' | 'completed' | 'cancelled' | 'announced';
  category: 'venture_capital' | 'private_equity' | 'corporate' | 'public_market';
  source?: string;
  confidence?: number;
}
