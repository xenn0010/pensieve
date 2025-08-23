# Globe Implementation Guide

## Overview

The Runway Navigator dashboard features an interactive 3D globe view powered by the 21st.dev globe component. This document provides comprehensive technical details for implementing, customizing, and extending the globe functionality.

## Architecture

### Component Structure
```
GlobeView (Main Container)
├── Globe Instance (21st.dev)
├── CompanyPoint Overlays
├── TransactionOverlay (Left Panel)
├── CompanyDrawer (Right Panel)
└── Globe Controls
```

### State Management
The globe state is managed through Zustand stores:
- `godmodeStore`: Controls globe mode, company selection, and configuration
- Company data: Mock data with real-world coordinates and business information

## 21st.dev Globe Integration

### Installation
```bash
npm install @21st/globe
```

### Basic Setup
```typescript
import { Globe } from '@21st/globe';

const globe = new Globe(containerElement, {
  backgroundColor: '#0f172a',
  atmosphereColor: '#1e40af',
  atmosphereAltitude: 0.15,
  enablePointerInteraction: true,
  enableInertia: true,
  autoRotate: true,
  autoRotateSpeed: 0.5
});
```

### Configuration Options

#### Core Settings
- `backgroundColor`: Globe background color
- `atmosphereColor`: Atmospheric glow color
- `atmosphereAltitude`: Height of atmospheric effect
- `enablePointerInteraction`: Enable mouse/touch interactions
- `enableInertia`: Smooth movement with momentum

#### Animation Settings
- `autoRotate`: Enable automatic rotation
- `autoRotateSpeed`: Rotation speed (0.1 - 2.0)
- `pointSize`: Size of data points
- `pointAltitude`: Height of points above surface
- `pointResolution`: Quality of point rendering

### Event Handling

#### Point Interactions
```typescript
// Click events
globe.on('pointClick', (event) => {
  const company = event.point.company;
  setSelectedCompany(company);
});

// Hover effects
globe.on('pointHover', (event) => {
  event.point.size = event.point.size * 1.5;
  globe.render();
});

globe.on('pointHoverEnd', (event) => {
  event.point.size = event.point.originalSize || 8;
  globe.render();
});
```

#### Camera Controls
```typescript
// Zoom to specific location
globe.controls().setZoom(2.0);

// Focus on coordinates
globe.controls().setLookAt(
  latitude, longitude, altitude,
  true // animate transition
);

// Reset view
globe.controls().reset();
```

## Company Data Integration

### Data Structure
```typescript
interface Company {
  id: string;
  name: string;
  coordinates: {
    lat: number;  // Latitude (-90 to 90)
    lng: number;  // Longitude (-180 to 180)
  };
  marketCap?: number;
  industry: string;
  signals: Signal[];
  riskLevel: 'low' | 'medium' | 'high';
  lastUpdated: Date;
}
```

### Point Visualization
```typescript
const pointsData = mockCompanies.map(company => ({
  lat: company.coordinates.lat,
  lng: company.coordinates.lng,
  size: getRiskSize(company.riskLevel),
  color: getRiskColor(company.riskLevel),
  company: company // Attach full company data
}));

function getRiskSize(riskLevel: string): number {
  switch (riskLevel) {
    case 'high': return 12;
    case 'medium': return 8;
    case 'low': return 6;
    default: return 8;
  }
}

function getRiskColor(riskLevel: string): string {
  switch (riskLevel) {
    case 'high': return '#ef4444';    // Red
    case 'medium': return '#f59e0b';  // Yellow
    case 'low': return '#10b981';     // Green
    default: return '#3b82f6';        // Blue
  }
}
```

## Interactive Features

### Company Selection
1. **Click Detection**: Globe points are clickable
2. **Data Retrieval**: Company information is extracted from point data
3. **Drawer Display**: Right-side panel shows company details
4. **State Update**: Selected company is stored in global state

### Hover Effects
- **Size Animation**: Points scale up on hover
- **Tooltip Display**: Company information appears above point
- **Visual Feedback**: Smooth transitions and animations

### Globe Controls
- **Auto-rotation Toggle**: Start/stop automatic rotation
- **View Reset**: Return to default camera position
- **Zoom Controls**: Mouse wheel and pinch gestures
- **Pan Navigation**: Click and drag to move view

## Performance Optimization

### Rendering Optimization
```typescript
// Debounce render calls
let renderTimeout: NodeJS.Timeout;
function debouncedRender() {
  clearTimeout(renderTimeout);
  renderTimeout = setTimeout(() => globe.render(), 16); // 60fps
}

// Use requestAnimationFrame for smooth animations
function animatePoint(point: any, targetSize: number) {
  const startSize = point.size;
  const startTime = performance.now();
  const duration = 300;

  function update(currentTime: number) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    point.size = startSize + (targetSize - startSize) * progress;
    globe.render();
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  
  requestAnimationFrame(update);
}
```

### Data Management
- **Lazy Loading**: Load company data on demand
- **Point Clustering**: Group nearby points for dense areas
- **Level of Detail**: Adjust point resolution based on zoom level
- **Memory Management**: Clean up unused resources

## Customization

### Theme Integration
```typescript
const theme = {
  light: {
    backgroundColor: '#ffffff',
    atmosphereColor: '#87ceeb',
    pointColors: {
      low: '#22c55e',
      medium: '#eab308',
      high: '#ef4444'
    }
  },
  dark: {
    backgroundColor: '#0f172a',
    atmosphereColor: '#1e40af',
    pointColors: {
      low: '#10b981',
      medium: '#f59e0b',
      high: '#ef4444'
    }
  }
};
```

### Animation Customization
```typescript
// Custom easing functions
const easing = {
  easeInOut: (t: number) => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
  easeOut: (t: number) => 1 - Math.pow(1 - t, 3),
  easeIn: (t: number) => t * t * t
};

// Apply custom animations
function animateCamera(target: any, duration: number = 1000) {
  const start = globe.controls().getLookAt();
  const startTime = performance.now();
  
  function update(currentTime: number) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easing.easeInOut(progress);
    
    const current = {
      lat: start.lat + (target.lat - start.lat) * eased,
      lng: start.lng + (target.lng - start.lng) * eased,
      altitude: start.altitude + (target.altitude - start.altitude) * eased
    };
    
    globe.controls().setLookAt(current.lat, current.lng, current.altitude, false);
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  
  requestAnimationFrame(update);
}
```

## Fallback Implementation

### Detection
```typescript
try {
  const { Globe } = await import('@21st/globe');
  // Initialize globe
} catch (error) {
  console.error('Failed to load globe component:', error);
  setGlobeInstance('fallback');
}
```

### Fallback UI
```typescript
if (globeInstance === 'fallback') {
  return (
    <div className="globe-container flex items-center justify-center">
      <div className="text-center">
        <div className="text-6xl mb-4">🌍</div>
        <h2 className="text-2xl font-bold text-white mb-2">Globe View</h2>
        <p className="text-dark-300 mb-6">
          Interactive 3D globe with company locations
        </p>
        {/* Grid of company cards for interaction */}
      </div>
    </div>
  );
}
```

## Testing

### Unit Tests
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import GlobeView from '../GlobeView';

describe('GlobeView', () => {
  test('renders fallback when globe fails to load', () => {
    render(<GlobeView />);
    expect(screen.getByText('Globe View')).toBeInTheDocument();
  });
  
  test('displays company information on point click', () => {
    // Test company selection functionality
  });
});
```

### Integration Tests
- Globe initialization
- Point interaction events
- State management integration
- Performance benchmarks

## Troubleshooting

### Common Issues

#### Globe Not Rendering
- Check WebGL support: `gl.getParameter(gl.VERSION)`
- Verify container element dimensions
- Check browser console for errors

#### Performance Issues
- Reduce point count for large datasets
- Implement point clustering
- Use `requestAnimationFrame` for animations
- Monitor memory usage

#### Interaction Problems
- Verify event listener registration
- Check point data structure
- Ensure proper coordinate ranges
- Test on different devices

### Debug Tools
```typescript
// Enable debug mode
const globe = new Globe(container, {
  ...config,
  debug: true
});

// Log globe state
console.log('Globe instance:', globe);
console.log('Camera position:', globe.controls().getLookAt());
console.log('Points data:', globe.getPointsData());
```

## Future Enhancements

### Advanced Features
- **Point Clustering**: Group nearby companies
- **Search & Filter**: Find companies by criteria
- **Time-based Data**: Historical company positions
- **3D Models**: Company logos and buildings
- **Path Visualization**: Connection lines between companies

### Performance Improvements
- **Web Workers**: Offload data processing
- **GPU Acceleration**: Use WebGL for complex calculations
- **Lazy Loading**: Load data progressively
- **Caching**: Store rendered frames

### Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: ARIA labels and descriptions
- **High Contrast**: Multiple color themes
- **Reduced Motion**: Respect user preferences

## Resources

- [21st.dev Globe Documentation](https://21st.dev/globe)
- [WebGL Fundamentals](https://webglfundamentals.org/)
- [Three.js Documentation](https://threejs.org/docs/)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)

---

This implementation provides a solid foundation for an interactive 3D globe view that can be extended with additional features and optimizations as needed.
