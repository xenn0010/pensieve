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
      size: isHighlighted ? baseSize * 1.5 : baseSize, // Highlighted pins are larger
      color: isHighlighted ? '#ffffff' : riskLevelColors[company.riskLevel as keyof typeof riskLevelColors], // Highlighted pins are white
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
    console.log('Search query:', query); // Debug log
    
    const lowerQuery = query.toLowerCase();
    const results: any[] = [];
    const highlighted = new Set<string>();

    // Search through companies
    mockCompanies.forEach(company => {
      let match = false;
      
      // Company name search
      if (company.name.toLowerCase().includes(lowerQuery)) {
        match = true;
        console.log('Company name match:', company.name);
      }
      
      // Location search (city names could be added to company data)
      if (company.coordinates.lat && company.coordinates.lng) {
        // Simple location search based on coordinates
        if (lowerQuery.includes('san francisco') && company.coordinates.lat > 37 && company.coordinates.lat < 38 && company.coordinates.lng > -123 && company.coordinates.lng < -122) {
          match = true;
          console.log('San Francisco match:', company.name);
        }
        if (lowerQuery.includes('london') && company.coordinates.lat > 51 && company.coordinates.lat < 52 && company.coordinates.lng > -1 && company.coordinates.lng < 0) {
          match = true;
          console.log('London match:', company.name);
        }
        if (lowerQuery.includes('tokyo') && company.coordinates.lat > 35 && company.coordinates.lat < 36 && company.coordinates.lng > 139 && company.coordinates.lng < 140) {
          match = true;
          console.log('Tokyo match:', company.name);
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
      
      if (match) {
        results.push(company);
        highlighted.add(company.id);
      }
    });

    console.log('Search results:', results.length, 'companies found');
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
              ${d.isHighlighted ? '<div style="color: #ffff00; font-weight: 600;">🔍 SEARCH RESULT</div>' : ''}
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
