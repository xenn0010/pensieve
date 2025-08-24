import { Company } from '../types/company';

export const mockCompanies: Company[] = [
  {
    id: '1',
    name: 'Brex',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 12000000000,
    industry: 'Financial Technology',
    riskLevel: 'low',
    signals: [
      {
        id: 's1',
        type: 'positive',
        category: 'financial',
        description: 'Series D funding round completed - $300M raised',
        severity: 4,
        timestamp: new Date('2024-01-15'),
        source: 'Funding Announcement',
        impact: 'Valuation increased to $12B, expansion into new markets'
      }
    ],
    lastUpdated: new Date(),
    description: 'Modern financial services platform for growing companies',
    website: 'https://brex.com',
    employees: 1200,
    founded: 2017
  },
  {
    id: '2',
    name: 'Cursor',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 8000000000,
    industry: 'Artificial Intelligence',
    riskLevel: 'low',
    signals: [
      {
        id: 's2',
        type: 'positive',
        category: 'operational',
        description: 'AI-powered code editor breakthrough - 40% productivity increase',
        severity: 4,
        timestamp: new Date('2024-01-20'),
        source: 'Product Launch',
        impact: 'User base grew 300% in Q4, enterprise adoption accelerating'
      }
    ],
    lastUpdated: new Date(),
    description: 'AI-first code editor that understands your codebase',
    website: 'https://cursor.sh',
    employees: 150,
    founded: 2022
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
    name: 'SpaceX',
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
  },
  {
    id: '9',
    name: 'Stripe',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 95000000000,
    industry: 'Financial Technology',
    riskLevel: 'low',
    signals: [
      {
        id: 's9',
        type: 'positive',
        category: 'financial',
        description: 'Record payment volume - $1T+ processed annually',
        severity: 5,
        timestamp: new Date('2024-01-24'),
        source: 'Financial Report',
        impact: 'Market leadership solidified, expanding to 50+ countries'
      }
    ],
    lastUpdated: new Date(),
    description: 'Global payment processing platform for internet businesses',
    website: 'https://stripe.com',
    employees: 8000,
    founded: 2010
  },
  {
    id: '10',
    name: 'OpenAI',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 80000000000,
    industry: 'Artificial Intelligence',
    riskLevel: 'medium',
    signals: [
      {
        id: 's10',
        type: 'positive',
        category: 'operational',
        description: 'GPT-5 development milestone reached',
        severity: 5,
        timestamp: new Date('2024-01-25'),
        source: 'Research Update',
        impact: 'AI capabilities advanced significantly, new partnerships formed'
      }
    ],
    lastUpdated: new Date(),
    description: 'Leading AI research and deployment company',
    website: 'https://openai.com',
    employees: 500,
    founded: 2015
  },
  {
    id: '11',
    name: 'Notion',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 10000000000,
    industry: 'Productivity Software',
    riskLevel: 'low',
    signals: [
      {
        id: 's11',
        type: 'positive',
        category: 'operational',
        description: 'Enterprise adoption surged 200%',
        severity: 4,
        timestamp: new Date('2024-01-26'),
        source: 'Business Update',
        impact: 'Large enterprise contracts driving growth'
      }
    ],
    lastUpdated: new Date(),
    description: 'All-in-one workspace for notes, docs, and collaboration',
    website: 'https://notion.so',
    employees: 300,
    founded: 2016
  },
  {
    id: '12',
    name: 'Figma',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 20000000000,
    industry: 'Design Software',
    riskLevel: 'low',
    signals: [
      {
        id: 's12',
        type: 'positive',
        category: 'operational',
        description: 'Collaborative design platform adoption growing',
        severity: 4,
        timestamp: new Date('2024-01-27'),
        source: 'Product Update',
        impact: 'Enterprise design teams migrating from competitors'
      }
    ],
    lastUpdated: new Date(),
    description: 'Collaborative interface design tool',
    website: 'https://figma.com',
    employees: 800,
    founded: 2012
  },
  {
    id: '13',
    name: 'Databricks',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 43000000000,
    industry: 'Data & Analytics',
    riskLevel: 'low',
    signals: [
      {
        id: 's13',
        type: 'positive',
        category: 'financial',
        description: 'Series I funding - $500M raised at $43B valuation',
        severity: 5,
        timestamp: new Date('2024-01-28'),
        source: 'Funding Announcement',
        impact: 'Expansion into AI and ML platforms'
      }
    ],
    lastUpdated: new Date(),
    description: 'Unified analytics platform for data engineering and ML',
    website: 'https://databricks.com',
    employees: 6000,
    founded: 2013
  },
  {
    id: '14',
    name: 'Snowflake',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 75000000000,
    industry: 'Cloud Data',
    riskLevel: 'medium',
    signals: [
      {
        id: 's14',
        type: 'neutral',
        category: 'market',
        description: 'Cloud data platform market leadership maintained',
        severity: 3,
        timestamp: new Date('2024-01-29'),
        source: 'Market Analysis',
        impact: 'Competitive position stable, new product launches planned'
      }
    ],
    lastUpdated: new Date(),
    description: 'Cloud-based data warehousing platform',
    website: 'https://snowflake.com',
    employees: 7000,
    founded: 2012
  },
  {
    id: '15',
    name: 'MongoDB',
    coordinates: { lat: 40.7128, lng: -74.0060 },
    marketCap: 35000000000,
    industry: 'Database',
    riskLevel: 'low',
    signals: [
      {
        id: 's15',
        type: 'positive',
        category: 'operational',
        description: 'Atlas cloud platform growth accelerating',
        severity: 4,
        timestamp: new Date('2024-01-30'),
        source: 'Earnings Call',
        impact: 'Cloud revenue up 60% YoY'
      }
    ],
    lastUpdated: new Date(),
    description: 'Modern database platform for applications',
    website: 'https://mongodb.com',
    employees: 5000,
    founded: 2007
  },
  {
    id: '16',
    name: 'Palantir',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 45000000000,
    industry: 'Data Analytics',
    riskLevel: 'medium',
    signals: [
      {
        id: 's16',
        type: 'positive',
        category: 'operational',
        description: 'Government contracts expanded to new regions',
        severity: 4,
        timestamp: '2024-01-31',
        source: 'Contract Announcement',
        impact: 'Revenue diversification, international expansion'
      }
    ],
    lastUpdated: new Date(),
    description: 'Data integration and analytics platform',
    website: 'https://palantir.com',
    employees: 4000,
    founded: 2003
  },
  {
    id: '17',
    name: 'Coinbase',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 25000000000,
    industry: 'Cryptocurrency',
    riskLevel: 'high',
    signals: [
      {
        id: 's17',
        type: 'negative',
        category: 'regulatory',
        description: 'Regulatory challenges in multiple jurisdictions',
        severity: 4,
        timestamp: new Date('2024-02-01'),
        source: 'Legal Update',
        impact: 'International expansion delayed, compliance costs increased'
      }
    ],
    lastUpdated: new Date(),
    description: 'Digital currency exchange and wallet platform',
    website: 'https://coinbase.com',
    employees: 3000,
    founded: 2012
  },
  {
    id: '18',
    name: 'Robinhood',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 15000000000,
    industry: 'Financial Technology',
    riskLevel: 'medium',
    signals: [
      {
        id: 's18',
        type: 'positive',
        category: 'operational',
        description: 'New investment products launched successfully',
        severity: 3,
        timestamp: new Date('2024-02-02'),
        source: 'Product Launch',
        impact: 'User engagement increased, new revenue streams'
      }
    ],
    lastUpdated: new Date(),
    description: 'Commission-free stock trading platform',
    website: 'https://robinhood.com',
    employees: 2500,
    founded: 2013
  },
  {
    id: '19',
    name: 'DoorDash',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 40000000000,
    industry: 'Food Delivery',
    riskLevel: 'medium',
    signals: [
      {
        id: 's19',
        type: 'positive',
        category: 'operational',
        description: 'International expansion to new markets',
        severity: 4,
        timestamp: new Date('2024-02-03'),
        source: 'Business Update',
        impact: 'Global footprint expanded, new partnerships formed'
      }
    ],
    lastUpdated: new Date(),
    description: 'Food delivery and logistics platform',
    website: 'https://doordash.com',
    employees: 8000,
    founded: 2013
  },
  {
    id: '20',
    name: 'Uber',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 120000000000,
    industry: 'Transportation',
    riskLevel: 'medium',
    signals: [
      {
        id: 's20',
        type: 'positive',
        category: 'financial',
        description: 'First profitable quarter achieved',
        severity: 5,
        timestamp: new Date('2024-02-04'),
        source: 'Earnings Report',
        impact: 'Path to profitability confirmed, investor confidence restored'
      }
    ],
    lastUpdated: new Date(),
    description: 'Global ride-sharing and delivery platform',
    website: 'https://uber.com',
    employees: 32000,
    founded: 2009
  },
  {
    id: '21',
    name: 'Airbnb',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 80000000000,
    industry: 'Travel & Hospitality',
    riskLevel: 'low',
    signals: [
      {
        id: 's21',
        type: 'positive',
        category: 'operational',
        description: 'Travel recovery driving strong bookings',
        severity: 4,
        timestamp: new Date('2024-02-05'),
        source: 'Business Update',
        impact: 'Revenue growth accelerated, new markets opened'
      }
    ],
    lastUpdated: new Date(),
    description: 'Global travel and accommodation platform',
    website: 'https://airbnb.com',
    employees: 6000,
    founded: 2008
  },
  {
    id: '22',
    name: 'Shopify',
    coordinates: { lat: 45.5017, lng: -73.5673 },
    marketCap: 100000000000,
    industry: 'E-commerce',
    riskLevel: 'low',
    signals: [
      {
        id: 's22',
        type: 'positive',
        category: 'operational',
        description: 'Enterprise e-commerce platform adoption growing',
        severity: 4,
        timestamp: new Date('2024-02-06'),
        source: 'Product Update',
        impact: 'Large enterprise customers driving growth'
      }
    ],
    lastUpdated: new Date(),
    description: 'E-commerce platform for online stores and retail',
    website: 'https://shopify.com',
    employees: 10000,
    founded: 2006
  },
  {
    id: '23',
    name: 'Spotify',
    coordinates: { lat: 59.3293, lng: 18.0686 },
    marketCap: 45000000000,
    industry: 'Entertainment',
    riskLevel: 'medium',
    signals: [
      {
        id: 's23',
        type: 'positive',
        category: 'operational',
        description: 'Premium subscriber growth exceeded expectations',
        severity: 4,
        timestamp: new Date('2024-02-07'),
        source: 'Earnings Call',
        impact: 'Revenue per user increased, profitability improved'
      }
    ],
    lastUpdated: new Date(),
    description: 'Digital music streaming and podcast platform',
    website: 'https://spotify.com',
    employees: 9000,
    founded: 2006
  },
  {
    id: '24',
    name: 'Zoom',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 25000000000,
    industry: 'Communication',
    riskLevel: 'medium',
    signals: [
      {
        id: 's24',
        type: 'neutral',
        category: 'market',
        description: 'Post-pandemic market stabilization',
        severity: 3,
        timestamp: new Date('2024-02-08'),
        source: 'Market Analysis',
        impact: 'Enterprise adoption steady, new features launched'
      }
    ],
    lastUpdated: new Date(),
    description: 'Video conferencing and communication platform',
    website: 'https://zoom.us',
    employees: 7000,
    founded: 2011
  },
  {
    id: '25',
    name: 'Slack',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    marketCap: 28000000000,
    industry: 'Communication',
    riskLevel: 'low',
    signals: [
      {
        id: 's25',
        type: 'positive',
        category: 'operational',
        description: 'Enterprise collaboration tools expanded',
        severity: 4,
        timestamp: new Date('2024-02-09'),
        source: 'Product Launch',
        impact: 'New enterprise features driving adoption'
      }
    ],
    lastUpdated: new Date(),
    description: 'Team communication and collaboration platform',
    website: 'https://slack.com',
    employees: 2500,
    founded: 2009
  },
  {
    id: '26',
    name: 'Klarna',
    coordinates: { lat: 59.3293, lng: 18.0686 },
    marketCap: 7000000000,
    industry: 'Financial Technology',
    riskLevel: 'medium',
    signals: [
      {
        id: 's26',
        type: 'positive',
        category: 'financial',
        description: 'BNPL market expansion in Europe and US',
        severity: 4,
        timestamp: new Date('2024-02-10'),
        source: 'Business Update',
        impact: 'Market share increased, new partnerships formed'
      }
    ],
    lastUpdated: new Date(),
    description: 'Buy now, pay later payment platform',
    website: 'https://klarna.com',
    employees: 5000,
    founded: 2005
  },
  {
    id: '27',
    name: 'Revolut',
    coordinates: { lat: 51.5074, lng: -0.1278 },
    marketCap: 33000000000,
    industry: 'Financial Technology',
    riskLevel: 'medium',
    signals: [
      {
        id: 's27',
        type: 'positive',
        category: 'operational',
        description: 'Global banking license obtained in multiple countries',
        severity: 4,
        timestamp: new Date('2024-02-11'),
        source: 'Regulatory Update',
        impact: 'Expansion into new markets, banking services launched'
      }
    ],
    lastUpdated: new Date(),
    description: 'Digital banking and financial services platform',
    website: 'https://revolut.com',
    employees: 6000,
    founded: 2015
  },
  {
    id: '28',
    name: 'TransferWise (Wise)',
    coordinates: { lat: 51.5074, lng: -0.1278 },
    marketCap: 11000000000,
    industry: 'Financial Technology',
    riskLevel: 'low',
    signals: [
      {
        id: 's28',
        type: 'positive',
        category: 'operational',
        description: 'International money transfer volume growing',
        severity: 4,
        timestamp: new Date('2024-02-12'),
        source: 'Business Update',
        impact: 'Revenue growth accelerated, new corridors opened'
      }
    ],
    lastUpdated: new Date(),
    description: 'International money transfer and currency exchange',
    website: 'https://wise.com',
    employees: 3000,
    founded: 2011
  },
  {
    id: '29',
    name: 'Deliveroo',
    coordinates: { lat: 51.5074, lng: -0.1278 },
    marketCap: 8000000000,
    industry: 'Food Delivery',
    riskLevel: 'medium',
    signals: [
      {
        id: 's29',
        type: 'positive',
        category: 'operational',
        description: 'European market expansion successful',
        severity: 3,
        timestamp: new Date('2024-02-13'),
        source: 'Business Update',
        impact: 'New markets opened, delivery network expanded'
      }
    ],
    lastUpdated: new Date(),
    description: 'Food delivery platform operating in Europe and Asia',
    website: 'https://deliveroo.co.uk',
    employees: 4000,
    founded: 2013
  },
  {
    id: '30',
    name: 'Nubank',
    coordinates: { lat: -23.5505, lng: -46.6333 },
    marketCap: 45000000000,
    industry: 'Financial Technology',
    riskLevel: 'low',
    signals: [
      {
        id: 's30',
        type: 'positive',
        category: 'financial',
        description: 'Latin America expansion accelerating',
        severity: 4,
        timestamp: new Date('2024-02-14'),
        source: 'Business Update',
        impact: 'New markets opened, customer base growing rapidly'
      }
    ],
    lastUpdated: new Date(),
    description: 'Digital banking platform for Latin America',
    website: 'https://nubank.com.br',
    employees: 7000,
    founded: 2013
  },
  {
    id: '31',
    name: 'Rappi',
    coordinates: { lat: 4.7110, lng: -74.0721 },
    marketCap: 25000000000,
    industry: 'Delivery & E-commerce',
    riskLevel: 'medium',
    signals: [
      {
        id: 's31',
        type: 'positive',
        category: 'operational',
        description: 'Super app ecosystem expanding in Latin America',
        severity: 4,
        timestamp: new Date('2024-02-15'),
        source: 'Product Launch',
        impact: 'New services launched, market penetration increased'
      }
    ],
    lastUpdated: new Date(),
    description: 'Latin American super app for delivery and services',
    website: 'https://rappi.com',
    employees: 5000,
    founded: 2015
  },
  {
    id: '32',
    name: 'Grab',
    coordinates: { lat: 1.3521, lng: 103.8198 },
    marketCap: 15000000000,
    industry: 'Transportation & Delivery',
    riskLevel: 'medium',
    signals: [
      {
        id: 's32',
        type: 'positive',
        category: 'operational',
        description: 'Southeast Asia super app ecosystem growing',
        severity: 4,
        timestamp: new Date('2024-02-16'),
        source: 'Business Update',
        impact: 'Financial services launched, market leadership maintained'
      }
    ],
    lastUpdated: new Date(),
    description: 'Southeast Asian super app for transport and services',
    website: 'https://grab.com',
    employees: 8000,
    founded: 2012
  },
  {
    id: '33',
    name: 'GoTo',
    coordinates: { lat: -6.2088, lng: 106.8456 },
    marketCap: 8000000000,
    industry: 'Technology',
    riskLevel: 'medium',
    signals: [
      {
        id: 's33',
        type: 'positive',
        category: 'operational',
        description: 'Indonesian tech ecosystem consolidation',
        severity: 3,
        timestamp: new Date('2024-02-17'),
        source: 'Business Update',
        impact: 'Market position strengthened, new services launched'
      }
    ],
    lastUpdated: new Date(),
    description: 'Indonesian technology company and digital ecosystem',
    website: 'https://goto.com',
    employees: 6000,
    founded: 2015
  },
  {
    id: '34',
    name: 'Paytm',
    coordinates: { lat: 28.7041, lng: 77.1025 },
    marketCap: 5000000000,
    industry: 'Financial Technology',
    riskLevel: 'medium',
    signals: [
      {
        id: 's34',
        type: 'positive',
        category: 'operational',
        description: 'Digital payments adoption accelerating in India',
        severity: 4,
        timestamp: new Date('2024-02-18'),
        source: 'Business Update',
        impact: 'User base growing, new financial products launched'
      }
    ],
    lastUpdated: new Date(),
    description: 'Indian digital payments and financial services platform',
    website: 'https://paytm.com',
    employees: 15000,
    founded: 2010
  },
  {
    id: '35',
    name: 'BYD',
    coordinates: { lat: 22.3193, lng: 114.1694 },
    marketCap: 80000000000,
    industry: 'Automotive & Energy',
    riskLevel: 'low',
    signals: [
      {
        id: 's35',
        type: 'positive',
        category: 'operational',
        description: 'Electric vehicle market leadership in China',
        severity: 5,
        timestamp: new Date('2024-02-19'),
        source: 'Sales Report',
        impact: 'EV sales record broken, international expansion accelerating'
      }
    ],
    lastUpdated: new Date(),
    description: 'Chinese electric vehicle and battery manufacturer',
    website: 'https://byd.com',
    employees: 300000,
    founded: 1995
  }
];

// Risk level color mapping for globe pins
export const riskLevelColors = {
  low: "#10B981",      // Green
  medium: "#F59E0B",   // Amber/Orange  
  high: "#EF4444"      // Red
};
