import React from 'react';
import { Company } from '../../types/company';

interface CompanyPointProps {
  company: Company;
  onClick: () => void;
}

const CompanyPoint: React.FC<CompanyPointProps> = ({ company, onClick }) => {
  const getRiskColor = (riskLevel: Company['riskLevel']) => {
    switch (riskLevel) {
      case 'high':
        return 'bg-red-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'low':
        return 'bg-green-500';
      default:
        return 'bg-blue-500';
    }
  };

  const getRiskSize = (riskLevel: Company['riskLevel']) => {
    switch (riskLevel) {
      case 'high':
        return 'w-4 h-4';
      case 'medium':
        return 'w-3 h-3';
      case 'low':
        return 'w-2 h-2';
      default:
        return 'w-3 h-3';
    }
  };

  return (
    <div
      className="absolute cursor-pointer group"
      style={{
        left: `${((company.coordinates.lng + 180) / 360) * 100}%`,
        top: `${((90 - company.coordinates.lat) / 180) * 100}%`,
        transform: 'translate(-50%, -50%)'
      }}
      onClick={onClick}
    >
      {/* Point */}
      <div
        className={`${getRiskColor(company.riskLevel)} ${getRiskSize(company.riskLevel)} rounded-full shadow-lg transition-all duration-200 group-hover:scale-150 group-hover:shadow-xl`}
      />
      
      {/* Pulse effect for high risk companies */}
      {company.riskLevel === 'high' && (
        <div className="absolute inset-0 rounded-full bg-red-500 animate-ping opacity-75" />
      )}
      
      {/* Tooltip */}
      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-dark-800/90 backdrop-blur-sm rounded-lg border border-dark-700 text-white text-sm whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10">
        <div className="font-medium">{company.name}</div>
        <div className="text-xs text-dark-300">{company.industry}</div>
        <div className="text-xs text-dark-300 capitalize">
          Risk: {company.riskLevel}
        </div>
        
        {/* Arrow */}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-dark-800/90" />
      </div>
    </div>
  );
};

export default CompanyPoint;
