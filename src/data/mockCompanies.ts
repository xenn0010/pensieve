import { Company } from '../types/company';

export const mockCompanies: Company[] = [
  {
    id: '1',
    name: 'TechCorp Inc',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 2500000000,
    industry: 'Technology',
    riskLevel: 'medium',
    signals: [
      {
        id: 's1',
        type: 'positive',
        category: 'financial',
        description: 'Strong Q4 earnings beat expectations',
        severity: 3,
        timestamp: new Date('2024-01-15'),
        source: 'Earnings Report',
        impact: 'Revenue growth 15% YoY'
      }
    ],
    lastUpdated: new Date(),
    description: 'Leading software company specializing in enterprise solutions',
    website: 'https://techcorp.com',
    employees: 2500,
    founded: 2010
  },
  {
    id: '2',
    name: 'GreenEnergy Ltd',
    coordinates: { lat: 51.5074, lng: -0.1278 },
    marketCap: 1800000000,
    industry: 'Renewable Energy',
    riskLevel: 'low',
    signals: [
      {
        id: 's2',
        type: 'positive',
        category: 'regulatory',
        description: 'New government subsidies for renewable energy',
        severity: 4,
        timestamp: new Date('2024-01-20'),
        source: 'Government Policy',
        impact: 'Expected 25% increase in project pipeline'
      }
    ],
    lastUpdated: new Date(),
    description: 'Sustainable energy solutions provider',
    website: 'https://greenenergy.co.uk',
    employees: 1200,
    founded: 2008
  },
  {
    id: '3',
    name: 'BioPharm Solutions',
    coordinates: { lat: 35.6762, lng: 139.6503 },
    marketCap: 3200000000,
    industry: 'Biotechnology',
    riskLevel: 'high',
    signals: [
      {
        id: 's3',
        type: 'negative',
        category: 'operational',
        description: 'Clinical trial phase 2 failure',
        severity: 5,
        timestamp: new Date('2024-01-18'),
        source: 'Clinical Results',
        impact: 'Stock price dropped 30%'
      }
    ],
    lastUpdated: new Date(),
    description: 'Innovative drug discovery and development',
    website: 'https://biopharm.jp',
    employees: 800,
    founded: 2012
  },
  {
    id: '4',
    name: 'FinTech Global',
    coordinates: { lat: 40.7128, lng: -74.0060 },
    marketCap: 1500000000,
    industry: 'Financial Technology',
    riskLevel: 'medium',
    signals: [
      {
        id: 's4',
        type: 'neutral',
        category: 'market',
        description: 'Partnership with major bank announced',
        severity: 2,
        timestamp: new Date('2024-01-22'),
        source: 'Press Release',
        impact: 'Market position strengthened'
      }
    ],
    lastUpdated: new Date(),
    description: 'Digital banking and payment solutions',
    website: 'https://fintechglobal.com',
    employees: 950,
    founded: 2015
  },
  {
    id: '5',
    name: 'AutoDrive Systems',
    coordinates: { lat: 48.8566, lng: 2.3522 },
    marketCap: 4200000000,
    industry: 'Automotive',
    riskLevel: 'medium',
    signals: [
      {
        id: 's5',
        type: 'positive',
        category: 'operational',
        description: 'New autonomous driving patent approved',
        severity: 4,
        timestamp: new Date('2024-01-19'),
        source: 'Patent Office',
        impact: 'Competitive advantage secured'
      }
    ],
    lastUpdated: new Date(),
    description: 'Advanced driver assistance and autonomous systems',
    website: 'https://autodrive.fr',
    employees: 2100,
    founded: 2009
  },
  {
    id: '6',
    name: 'CloudNet Solutions',
    coordinates: { lat: -33.8688, lng: 151.2093 },
    marketCap: 2800000000,
    industry: 'Cloud Computing',
    riskLevel: 'low',
    signals: [
      {
        id: 's6',
        type: 'positive',
        category: 'financial',
        description: 'Record quarterly cloud revenue',
        severity: 3,
        timestamp: new Date('2024-01-21'),
        source: 'Earnings Call',
        impact: 'Cloud segment growth 40% YoY'
      }
    ],
    lastUpdated: new Date(),
    description: 'Enterprise cloud infrastructure and services',
    website: 'https://cloudnet.au',
    employees: 1800,
    founded: 2011
  },
  {
    id: '7',
    name: 'Quantum Computing Corp',
    coordinates: { lat: 55.6761, lng: 12.5683 },
    marketCap: 950000000,
    industry: 'Quantum Technology',
    riskLevel: 'high',
    signals: [
      {
        id: 's7',
        type: 'positive',
        category: 'operational',
        description: 'Breakthrough in qubit stability',
        severity: 5,
        timestamp: new Date('2024-01-17'),
        source: 'Research Publication',
        impact: 'Technology leadership position'
      }
    ],
    lastUpdated: new Date(),
    description: 'Next-generation quantum computing hardware',
    website: 'https://quantum.dk',
    employees: 450,
    founded: 2018
  },
  {
    id: '8',
    name: 'SpaceX Technologies',
    coordinates: { lat: 25.7617, lng: -80.1918 },
    marketCap: 15000000000,
    industry: 'Aerospace',
    riskLevel: 'medium',
    signals: [
      {
        id: 's8',
        type: 'positive',
        category: 'operational',
        description: 'Successful satellite constellation deployment',
        severity: 4,
        timestamp: new Date('2024-01-23'),
        source: 'Mission Control',
        impact: 'Revenue from satellite services increased'
      }
    ],
    lastUpdated: new Date(),
    description: 'Space exploration and satellite technology',
    website: 'https://spacex.com',
    employees: 12000,
    founded: 2002
  }
];

// Risk level color mapping for globe pins
export const riskLevelColors = {
  low: "#10B981",      // Green
  medium: "#F59E0B",   // Amber/Orange  
  high: "#EF4444"      // Red
};
