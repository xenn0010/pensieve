// Test script to verify search functionality
const mockCompanies = [
  {
    id: '1',
    name: 'Brex',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    industry: 'Financial Technology',
    riskLevel: 'low'
  },
  {
    id: '2',
    name: 'Cursor',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    industry: 'Artificial Intelligence',
    riskLevel: 'low'
  },
  {
    id: '3',
    name: 'Stripe',
    coordinates: { lat: 37.7749, lng: -122.4194 },
    industry: 'Financial Technology',
    riskLevel: 'low'
  },
  {
    id: '4',
    name: 'MongoDB',
    coordinates: { lat: 40.7128, lng: -74.0060 },
    industry: 'Database',
    riskLevel: 'low'
  },
  {
    id: '5',
    name: 'Revolut',
    coordinates: { lat: 51.5074, lng: -0.1278 },
    industry: 'Financial Technology',
    riskLevel: 'medium'
  }
];

// Test search function
function testSearch(query) {
  console.log(`\n🔍 Testing search for: "${query}"`);
  
  const lowerQuery = query.toLowerCase().trim();
  const results = [];
  
  mockCompanies.forEach(company => {
    let match = false;
    let matchReason = '';
    
    // Company name search
    if (company.name.toLowerCase().includes(lowerQuery)) {
      match = true;
      matchReason = 'Company name';
    }
    
    // Location search
    if (lowerQuery.includes('san francisco') || lowerQuery.includes('sf') || lowerQuery.includes('bay area')) {
      if (company.coordinates.lat > 37 && company.coordinates.lat < 38 && company.coordinates.lng > -123 && company.coordinates.lng < -122) {
        match = true;
        matchReason = 'San Francisco location';
      }
    }
    
    if (lowerQuery.includes('new york') || lowerQuery.includes('nyc')) {
      if (company.coordinates.lat > 40 && company.coordinates.lat < 41 && company.coordinates.lng > -74 && company.coordinates.lng < -73) {
        match = true;
        matchReason = 'New York location';
      }
    }
    
    if (lowerQuery.includes('london') || lowerQuery.includes('uk')) {
      if (company.coordinates.lat > 51 && company.coordinates.lat < 52 && company.coordinates.lng > -1 && company.coordinates.lng < 0) {
        match = true;
        matchReason = 'London location';
      }
    }
    
    // Industry search
    if (company.industry.toLowerCase().includes(lowerQuery)) {
      match = true;
      matchReason = 'Industry';
    }
    
    // Risk level search
    if (lowerQuery.includes('low risk') && company.riskLevel === 'low') {
      match = true;
      matchReason = 'Low risk';
    }
    
    if (match) {
      results.push({ ...company, matchReason });
    }
  });
  
  console.log(`✅ Found ${results.length} results:`);
  results.forEach((result, index) => {
    console.log(`  ${index + 1}. ${result.name} - ${result.matchReason}`);
  });
  
  return results;
}

// Run tests
console.log('🧪 Testing Search Functionality\n');

testSearch('Brex');
testSearch('SF');
testSearch('Fintech');
testSearch('London');
testSearch('New York');
testSearch('low risk');
testSearch('AI');
testSearch('Database');
testSearch('Cursor');
testSearch('Stripe');

console.log('\n✅ Search tests completed!');
