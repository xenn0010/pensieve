import React, { useRef, useEffect, useState, useCallback } from 'react';
import Globe from 'react-globe.gl';
import { useGodmodeStore } from '../../store/godmodeStore';
import { mockCompanies, riskLevelColors } from '../../data/mockCompanies';
import TransactionOverlay from './TransactionOverlay';
import CompanyDrawer from './CompanyDrawer';
import FooterSearchBar from './FooterSearchBar';
import Header from '../layout/Header';

const GlobeView: React.FC = () => {
  const { selectedCompany, setSelectedCompany, globeConfig } = useGodmodeStore();
  const globeRef = useRef<any>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const [highlightedCompanies, setHighlightedCompanies] = useState<Set<string>>(new Set());

  // Update dimensions on mount and resize
  useEffect(() => {
    const updateDimensions = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  // Convert company data to globe.gl format with proper pin markers and highlighting
  const pointsData = mockCompanies.map(company => {
    const isHighlighted = highlightedCompanies.has(company.id);
    const baseSize = company.riskLevel === 'high' ? 1.2 : company.riskLevel === 'medium' ? 1.0 : 0.8;
    
    return {
      lat: company.coordinates.lat,
      lng: company.coordinates.lng,
      size: isHighlighted ? baseSize * 2.0 : baseSize, // Highlighted pins are much larger
      color: isHighlighted ? '#ffff00' : riskLevelColors[company.riskLevel as keyof typeof riskLevelColors], // Highlighted pins are bright yellow
      name: company.name,
      industry: company.industry,
      riskLevel: company.riskLevel,
      company: company, // Store full company data
      isHighlighted: isHighlighted
    };
  });

  // Handle point click
  const onPointClick = useCallback((point: any) => {
    if (point.company) {
      setSelectedCompany(point.company);
    }
  }, [setSelectedCompany]);

  // Handle globe click
  const onGlobeClick = useCallback(() => {
    // Clear selection when clicking on empty space
    setSelectedCompany(null);
  }, [setSelectedCompany]);

  // Handle point hover
  const onPointHover = useCallback((point: any) => {
    if (point) {
      // Highlight hovered point
      if (document.body) {
        document.body.style.cursor = 'pointer';
      }
    } else {
      if (document.body) {
        document.body.style.cursor = 'default';
      }
    }
  }, []);

    // Handle search queries
  const handleSearch = useCallback((query: string) => {
    console.log('🔍 Search query:', query); // Debug log
    
    const lowerQuery = query.toLowerCase().trim();
    const results: any[] = [];
    const highlighted = new Set<string>();

    if (!lowerQuery) {
      console.log('Empty query, clearing highlights');
      setHighlightedCompanies(new Set());
      return;
    }

    // Search through companies
    mockCompanies.forEach(company => {
      let match = false;
      let matchReason = '';
      
      // Company name search (exact and partial)
      if (company.name.toLowerCase().includes(lowerQuery)) {
        match = true;
        matchReason = 'Company name';
        console.log('✅ Company name match:', company.name);
      }
      
      // Company name exact match (higher priority)
      if (company.name.toLowerCase() === lowerQuery) {
        match = true;
        matchReason = 'Exact company name';
        console.log('🎯 EXACT Company name match:', company.name);
      }
      
      // Location search (city names could be added to company data)
      if (company.coordinates.lat && company.coordinates.lng) {
        // San Francisco Bay Area
        if (lowerQuery.includes('san francisco') || lowerQuery.includes('sf') || lowerQuery.includes('bay area') || lowerQuery.includes('silicon valley')) {
          if (company.coordinates.lat > 37 && company.coordinates.lat < 38 && company.coordinates.lng > -123 && company.coordinates.lng < -122) {
            match = true;
            matchReason = 'San Francisco location';
            console.log('📍 San Francisco match:', company.name);
          }
        }
        // New York
        if (lowerQuery.includes('new york') || lowerQuery.includes('nyc') || lowerQuery.includes('manhattan')) {
          if (company.coordinates.lat > 40 && company.coordinates.lat < 41 && company.coordinates.lng > -74 && company.coordinates.lng < -73) {
            match = true;
            matchReason = 'New York location';
            console.log('📍 New York match:', company.name);
          }
        }
        // London
        if (lowerQuery.includes('london') || lowerQuery.includes('uk') || lowerQuery.includes('england')) {
          if (company.coordinates.lat > 51 && company.coordinates.lat < 52 && company.coordinates.lng > -1 && company.coordinates.lng < 0) {
            match = true;
            matchReason = 'London location';
            console.log('📍 London match:', company.name);
          }
        }
        // Tokyo
        if (lowerQuery.includes('tokyo') || lowerQuery.includes('japan')) {
          if (company.coordinates.lat > 35 && company.coordinates.lat < 36 && company.coordinates.lng > 139 && company.coordinates.lng < 140) {
            match = true;
            console.log('Tokyo match:', company.name);
          }
        }
        // Paris
        if (lowerQuery.includes('paris') || lowerQuery.includes('france')) {
          if (company.coordinates.lat > 48 && company.coordinates.lat < 49 && company.coordinates.lng > 2 && company.coordinates.lng < 3) {
            match = true;
            console.log('Paris match:', company.name);
          }
        }
        // Sydney
        if (lowerQuery.includes('sydney') || lowerQuery.includes('australia')) {
          if (company.coordinates.lat > -34 && company.coordinates.lat < -33 && company.coordinates.lng > 151 && company.coordinates.lng < 152) {
            match = true;
            console.log('Sydney match:', company.name);
          }
        }
        // Copenhagen
        if (lowerQuery.includes('copenhagen') || lowerQuery.includes('denmark')) {
          if (company.coordinates.lat > 55 && company.coordinates.lat < 56 && company.coordinates.lng > 12 && company.coordinates.lng < 13) {
            match = true;
            console.log('Copenhagen match:', company.name);
          }
        }
        // Miami
        if (lowerQuery.includes('miami') || lowerQuery.includes('florida')) {
          if (company.coordinates.lat > 25 && company.coordinates.lat < 26 && company.coordinates.lng > -81 && company.coordinates.lng < -80) {
            match = true;
            console.log('Miami match:', company.name);
          }
        }
        // Montreal
        if (lowerQuery.includes('montreal') || lowerQuery.includes('canada')) {
          if (company.coordinates.lat > 45 && company.coordinates.lat < 46 && company.coordinates.lng > -74 && company.coordinates.lng < -73) {
            match = true;
            console.log('Montreal match:', company.name);
          }
        }
        // Stockholm
        if (lowerQuery.includes('stockholm') || lowerQuery.includes('sweden')) {
          if (company.coordinates.lat > 59 && company.coordinates.lat < 60 && company.coordinates.lng > 18 && company.coordinates.lng < 19) {
            match = true;
            console.log('Stockholm match:', company.name);
          }
        }
        // São Paulo
        if (lowerQuery.includes('sao paulo') || lowerQuery.includes('brazil')) {
          if (company.coordinates.lat > -24 && company.coordinates.lat < -23 && company.coordinates.lng > -47 && company.coordinates.lng < -46) {
            match = true;
            console.log('São Paulo match:', company.name);
          }
        }
        // Bogotá
        if (lowerQuery.includes('bogota') || lowerQuery.includes('colombia')) {
          if (company.coordinates.lat > 4 && company.coordinates.lat < 5 && company.coordinates.lng > -75 && company.coordinates.lng < -74) {
            match = true;
            console.log('Bogotá match:', company.name);
          }
        }
        // Singapore
        if (lowerQuery.includes('singapore')) {
          if (company.coordinates.lat > 1 && company.coordinates.lat < 2 && company.coordinates.lng > 103 && company.coordinates.lng < 104) {
            match = true;
            console.log('Singapore match:', company.name);
          }
        }
        // Jakarta
        if (lowerQuery.includes('jakarta') || lowerQuery.includes('indonesia')) {
          if (company.coordinates.lat > -7 && company.coordinates.lat < -6 && company.coordinates.lng > 106 && company.coordinates.lng < 107) {
            match = true;
            console.log('Jakarta match:', company.name);
          }
        }
        // New Delhi
        if (lowerQuery.includes('delhi') || lowerQuery.includes('india')) {
          if (company.coordinates.lat > 28 && company.coordinates.lat < 29 && company.coordinates.lng > 77 && company.coordinates.lng < 78) {
            match = true;
            console.log('New Delhi match:', company.name);
          }
        }
        // Hong Kong
        if (lowerQuery.includes('hong kong') || lowerQuery.includes('china')) {
          if (company.coordinates.lat > 22 && company.coordinates.lat < 23 && company.coordinates.lng > 114 && company.coordinates.lng < 115) {
            match = true;
            console.log('Hong Kong match:', company.name);
          }
        }
      }
      
      // Risk level search
      if (lowerQuery.includes('high risk') && company.riskLevel === 'high') {
        match = true;
        console.log('High risk match:', company.name);
      }
      if (lowerQuery.includes('low risk') && company.riskLevel === 'low') {
        match = true;
        console.log('Low risk match:', company.name);
      }
      if (lowerQuery.includes('medium risk') && company.riskLevel === 'medium') {
        match = true;
        console.log('Medium risk match:', company.name);
      }
      
      // Industry search
      if (company.industry.toLowerCase().includes(lowerQuery)) {
        match = true;
        console.log('Industry match:', company.name, company.industry);
      }
      
      // Enhanced industry search with aliases
      const industryAliases: { [key: string]: string[] } = {
        'fintech': ['financial technology', 'financial tech'],
        'ai': ['artificial intelligence', 'machine learning', 'ml'],
        'saas': ['software as a service', 'cloud software'],
        'ecommerce': ['e-commerce', 'online retail', 'digital commerce'],
        'crypto': ['cryptocurrency', 'blockchain', 'digital currency'],
        'biotech': ['biotechnology', 'life sciences', 'pharmaceuticals'],
        'cloud': ['cloud computing', 'cloud infrastructure', 'cloud services'],
        'data': ['data analytics', 'big data', 'data science'],
        'design': ['design software', 'creative tools', 'ui/ux'],
        'productivity': ['productivity software', 'collaboration tools', 'workflow'],
        'transport': ['transportation', 'mobility', 'logistics'],
        'food': ['food delivery', 'restaurant tech', 'food tech'],
        'travel': ['travel & hospitality', 'accommodation', 'tourism'],
        'entertainment': ['media', 'streaming', 'content'],
        'communication': ['communication tools', 'messaging', 'video conferencing']
      };
      
      // Check industry aliases
      for (const [alias, industries] of Object.entries(industryAliases)) {
        if (lowerQuery.includes(alias) && industries.some(ind => company.industry.toLowerCase().includes(ind))) {
          match = true;
          console.log('Industry alias match:', company.name, company.industry, 'via', alias);
          break;
        }
      }
      
      if (match) {
        results.push({
          ...company,
          matchReason,
          matchScore: company.name.toLowerCase() === lowerQuery ? 100 : 
                     company.name.toLowerCase().startsWith(lowerQuery) ? 90 :
                     company.name.toLowerCase().includes(lowerQuery) ? 80 : 70
        });
        highlighted.add(company.id);
      }
    });

    // Sort results by relevance (exact matches first, then partial matches)
    results.sort((a, b) => b.matchScore - a.matchScore);

    console.log('🔍 Search results:', results.length, 'companies found');
    results.forEach((result, index) => {
      console.log(`${index + 1}. ${result.name} (${result.matchReason}) - Score: ${result.matchScore}`);
    });
    
    setHighlightedCompanies(highlighted);

    // If we found results, fly to the first one
    if (results.length > 0 && globeRef.current && globeRef.current.pointOfView) {
      const firstResult = results[0];
      console.log('Flying to:', firstResult.name, 'at', firstResult.coordinates);
      
      globeRef.current.pointOfView(
        { 
          lat: firstResult.coordinates.lat, 
          lng: firstResult.coordinates.lng, 
          altitude: 2.0 
        }, 
        2000 // 2 second animation
      );
      
      // Set the selected company to show details
      setSelectedCompany(firstResult);
    } else {
      console.log('No results found for query:', query);
    }
  }, [setSelectedCompany]);

  // Auto-rotation control
  useEffect(() => {
    if (globeRef.current && globeRef.current.controls) {
      const controls = globeRef.current.controls();
      if (controls) {
        controls.autoRotate = globeConfig.autoRotate;
        controls.autoRotateSpeed = 0.5;
      }
    }
  }, [globeConfig.autoRotate]);

  return (
    <div className="globe-container relative w-full h-full overflow-hidden">
      {/* Responsive layout container */}
      <div className="relative w-full h-full">
      {/* Globe Component - Full background covering entire viewport */}
      <div className="absolute inset-0">
        <Globe
          ref={globeRef}
          width={dimensions.width}
          height={dimensions.height}
          backgroundColor={globeConfig.backgroundColor}
          atmosphereColor="#1e40af"
          atmosphereAltitude={0.15}
          showAtmosphere={true}
          showGlobe={true}
          showGraticules={false}
          enablePointerInteraction={true}
          pointsData={pointsData}
          pointLat="lat"
          pointLng="lng"
          pointColor="color"
          pointRadius="size"
          pointAltitude={0.02}
          pointResolution={16}
          pointLabel={(d: any) => `
            <div style="color: white; background: rgba(0,0,0,0.9); padding: 10px; border-radius: 6px; font-size: 12px; border: 2px solid ${d.color}; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
              <div style="font-weight: bold; color: ${d.color};">${d.name}</div>
              <div style="color: #ccc;">${d.industry}</div>
              <div style="color: ${d.color}; font-weight: 600;">Risk: ${d.riskLevel.toUpperCase()}</div>
              ${d.isHighlighted ? '<div style="color: #ffff00; font-weight: 600; text-shadow: 0 0 10px #ffff00;">🔍 SEARCH RESULT</div>' : ''}
            </div>
          `}
          onPointClick={onPointClick}
          onGlobeClick={onGlobeClick}
          onPointHover={onPointHover}
          globeImageUrl="https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
          bumpImageUrl="https://unpkg.com/three-globe/example/img/earth-topology.png"
          waitForGlobeReady={true}
          animateIn={true}
        />
      </div>

      {/* Header - Now positioned above the globe background */}
      <div className="relative z-40">
        <Header />
      </div>

      {/* Left Side - Transaction Overlay */}
      <TransactionOverlay />

      {/* Footer Search Bar */}
      <FooterSearchBar 
        onSearch={handleSearch} 
        onClear={() => {
          setHighlightedCompanies(new Set());
          setSelectedCompany(null);
        }}
        hasResults={highlightedCompanies.size > 0}
      />

      {/* Right Side - Company Drawer */}
      <CompanyDrawer
        company={selectedCompany}
        onClose={() => setSelectedCompany(null)}
      />

      
      </div>
    </div>
  );
};

export default GlobeView;
