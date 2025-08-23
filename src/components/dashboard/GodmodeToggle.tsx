import React from 'react';
import { Globe, Grid3X3 } from 'lucide-react';
import { useGodmodeStore } from '../../store/godmodeStore';

const GodmodeToggle: React.FC = () => {
  const { isActive, toggleGodmode } = useGodmodeStore();

  return (
    <button
      onClick={toggleGodmode}
              className={`
          flex items-center gap-3 px-6 py-3 rounded-xl font-medium transition-all duration-300 backdrop-blur-md
          ${isActive 
            ? 'bg-primary-600/90 text-white shadow-lg shadow-primary-600/25' 
            : 'bg-dark-700/60 text-dark-300 hover:bg-dark-600/60 hover:text-white'
          }
        `}
    >
      {isActive ? (
        <>
          <Grid3X3 className="w-5 h-5" />
          <span>Normal Mode</span>
        </>
      ) : (
        <>
          <Globe className="w-5 h-5" />
          <span>Godmode</span>
        </>
      )}
    </button>
  );
};

export default GodmodeToggle;
