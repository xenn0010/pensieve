import React, { useState } from 'react';
import { X, Globe, Building2, Users, Calendar, ExternalLink, AlertTriangle, CheckCircle, Info, Maximize2, Minimize2 } from 'lucide-react';
import { Company } from '../../types/company';

interface CompanyDrawerProps {
  company: Company | null;
  onClose: () => void;
}

const CompanyDrawer: React.FC<CompanyDrawerProps> = ({ company, onClose }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  if (!company) return null;

  const getRiskColor = (riskLevel: Company['riskLevel']) => {
    switch (riskLevel) {
      case 'high':
        return 'text-red-400 bg-red-500/20 border-red-500/30';
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30';
      case 'low':
        return 'text-green-400 bg-green-500/20 border-green-500/30';
      default:
        return 'text-blue-400 bg-blue-500/20 border-blue-500/30';
    }
  };

  const getSignalIcon = (type: string) => {
    switch (type) {
      case 'positive':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'negative':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'neutral':
        return <Info className="w-4 h-4 text-blue-500" />;
      default:
        return <Info className="w-4 h-4 text-gray-500" />;
    }
  };

  const getSignalColor = (type: string) => {
    switch (type) {
      case 'positive':
        return 'border-green-500/30 bg-green-500/10';
      case 'negative':
        return 'border-red-500/30 bg-red-500/10';
      case 'neutral':
        return 'border-blue-500/30 bg-blue-500/10';
      default:
        return 'border-gray-500/30 bg-gray-500/10';
    }
  };

  const formatMarketCap = (marketCap?: number) => {
    if (!marketCap) return 'N/A';
    
    const formatter = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      notation: 'compact',
      maximumFractionDigits: 1,
    });
    
    return formatter.format(marketCap);
  };

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  };

  return (
    <div className={`absolute right-6 top-40 ${
      isExpanded 
        ? 'inset-0 w-full h-full' 
        : 'w-80 max-h-[calc(100vh-10rem)]'
    } bg-dark-800/95 backdrop-blur-md border border-dark-700 shadow-2xl overflow-hidden transition-all duration-300 ease-in-out ${
      isExpanded ? 'z-50 rounded-none' : 'z-30 rounded-xl'
    } ${
      company ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-full pointer-events-none'
    }`}>
      {/* Header - Connected seamlessly to content */}
      <div className={`p-6 bg-dark-800/50 ${isExpanded ? 'border-b border-dark-700' : 'rounded-t-xl'}`}>
        <div className="flex items-center justify-between mb-4">
          <h2 className={`font-bold text-white ${isExpanded ? 'text-3xl' : 'text-xl'}`}>
            {company.name}
          </h2>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="p-2 hover:bg-dark-700 rounded-lg transition-colors"
              title={isExpanded ? "Collapse view" : "Expand to full page"}
            >
              {isExpanded ? (
                <Minimize2 className="w-5 h-5 text-dark-300" />
              ) : (
                <Maximize2 className="w-5 h-5 text-dark-300" />
              )}
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-dark-700 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-dark-300" />
            </button>
          </div>
        </div>
        
        <div className="flex items-center gap-3 mb-3">
          <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getRiskColor(company.riskLevel)}`}>
            {company.riskLevel.toUpperCase()} RISK
          </span>
          <span className="text-sm text-dark-300">{company.industry}</span>
        </div>
        
        {company.description && (
          <p className="text-dark-200 text-sm leading-relaxed">
            {company.description}
          </p>
        )}
        
        {isExpanded && (
          <div className="mt-4 p-3 bg-dark-800/30 rounded-lg border border-dark-700">
            <p className="text-xs text-dark-300 text-center">
              📊 Full Company Profile View - Scroll to explore all details
            </p>
          </div>
        )}
      </div>

      {/* Company Details - Scrollable content */}
      <div className={`p-6 space-y-6 bg-dark-800/30 overflow-y-auto company-drawer-scroll ${
        isExpanded 
          ? 'max-h-[calc(100vh-4rem)] rounded-none' 
          : 'max-h-80 rounded-b-xl'
      }`}>

        
        {/* Key Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <div className="flex items-center gap-2 mb-2">
              <Building2 className="w-4 h-4 text-primary-500" />
              <span className="text-sm text-dark-300">Market Cap</span>
            </div>
            <div className="text-lg font-semibold text-white">
              {formatMarketCap(company.marketCap)}
            </div>
          </div>
          
          <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <div className="flex items-center gap-2 mb-2">
              <Users className="w-4 h-4 text-primary-500" />
              <span className="text-sm text-dark-300">Employees</span>
            </div>
            <div className="text-lg font-semibold text-white">
              {company.employees?.toLocaleString() || 'N/A'}
            </div>
          </div>
          
          <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="w-4 h-4 text-primary-500" />
              <span className="text-sm text-dark-300">Founded</span>
            </div>
            <div className="text-lg font-semibold text-white">
              {company.founded || 'N/A'}
            </div>
          </div>
          
          <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <div className="flex items-center gap-2 mb-2">
              <Globe className="w-4 h-4 text-primary-500" />
              <span className="text-sm text-dark-300">Location</span>
            </div>
            <div className="text-sm text-white">
              {company.coordinates.lat.toFixed(2)}°, {company.coordinates.lng.toFixed(2)}°
            </div>
          </div>
        </div>

        {/* Market Signals */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Market Signals</h3>
          <div className="space-y-3">
            {company.signals.map((signal) => (
              <div
                key={signal.id}
                className={`p-4 rounded-lg border ${getSignalColor(signal.type)}`}
              >
                <div className="flex items-start gap-3">
                  {getSignalIcon(signal.type)}
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h4 className="text-sm font-medium text-white capitalize">
                        {signal.category}
                      </h4>
                      <span className="text-xs text-dark-300">
                        Severity: {signal.severity}/5
                      </span>
                    </div>
                    <p className="text-sm text-dark-200 mb-2">
                      {signal.description}
                    </p>
                    <div className="flex items-center justify-between text-xs text-dark-400">
                      <span>Source: {signal.source}</span>
                      <span>{formatDate(signal.timestamp)}</span>
                    </div>
                    {signal.impact && (
                      <div className="mt-2 text-xs text-primary-400">
                        Impact: {signal.impact}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Website Link */}
        {company.website && (
          <div className="pt-4 border-t border-dark-700">
            <a
              href={company.website}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-colors"
            >
              <ExternalLink className="w-4 h-4" />
              Visit Website
            </a>
          </div>
        )}
        
        {/* Bottom Fade Indicator */}
        <div className="sticky bottom-0 -mb-6 pb-8 pt-2 bg-gradient-to-t from-dark-800/30 to-transparent pointer-events-none z-10">
          <div className="text-xs text-dark-400 text-center opacity-60">
            ✨ End of company details
          </div>
        </div>
        
        {/* Bottom Spacing */}
        <div className="h-8"></div>
        
        {/* Additional Company Information */}
        <div className="space-y-4">
          <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <h4 className="text-sm font-semibold text-white mb-2">Financial Performance</h4>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div>
                <span className="text-dark-300">Revenue Growth:</span>
                <span className="text-green-400 ml-2">+15.2% YoY</span>
              </div>
              <div>
                <span className="text-dark-300">Profit Margin:</span>
                <span className="text-blue-400 ml-2">12.8%</span>
              </div>
              <div>
                <span className="text-dark-300">Cash Flow:</span>
                <span className="text-green-400 ml-2">$2.1B</span>
              </div>
              <div>
                <span className="text-dark-300">Debt Ratio:</span>
                <span className="text-yellow-400 ml-2">0.34</span>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <h4 className="text-sm font-semibold text-white mb-2">Recent Developments</h4>
            <div className="space-y-2 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-dark-200">New product launch in Q4 2024</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-dark-200">Strategic partnership announced</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <span className="text-dark-200">Expansion into new markets</span>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <h4 className="text-sm font-semibold text-white mb-2">Competitive Analysis</h4>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-dark-300">Market Share:</span>
                <span className="text-white">23.4%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-dark-300">Competitors:</span>
                <span className="text-white">5 major players</span>
              </div>
              <div className="flex justify-between">
                <span className="text-dark-300">Industry Rank:</span>
                <span className="text-white">#2</span>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <h4 className="text-sm font-semibold text-white mb-2">Risk Assessment</h4>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-dark-300">Regulatory Risk:</span>
                <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded text-xs">Medium</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-dark-300">Market Risk:</span>
                <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">Low</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-dark-300">Operational Risk:</span>
                <span className="px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs">High</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompanyDrawer;
