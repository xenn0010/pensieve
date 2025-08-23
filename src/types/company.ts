export interface Company {
  id: string;
  name: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  marketCap?: number;
  industry: string;
  signals: Signal[];
  riskLevel: 'low' | 'medium' | 'high';
  lastUpdated: Date;
  description?: string;
  website?: string;
  employees?: number;
  founded?: number;
}

export interface Signal {
  id: string;
  type: 'positive' | 'negative' | 'neutral';
  category: 'financial' | 'operational' | 'market' | 'regulatory';
  description: string;
  severity: 1 | 2 | 3 | 4 | 5;
  timestamp: Date;
  source: string;
  impact?: string;
}
