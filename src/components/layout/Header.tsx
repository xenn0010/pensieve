import React from 'react';
import KPICards from '../dashboard/KPICards';
import GodmodeToggle from '../dashboard/GodmodeToggle';
import { useGodmodeStore } from '../../store/godmodeStore';

const Header: React.FC = () => {
  const { isActive } = useGodmodeStore();
  
  return (
    <header className={`relative z-40 p-6 ${
      isActive 
        ? 'bg-transparent border-none' 
        : 'bg-dark-800/95 backdrop-blur-md border-b border-dark-700/50'
    }`}>
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div className="flex-1">
          <KPICards />
        </div>
        <div className="flex justify-center lg:justify-end">
          <GodmodeToggle />
        </div>
      </div>
    </header>
  );
};

export default Header;
