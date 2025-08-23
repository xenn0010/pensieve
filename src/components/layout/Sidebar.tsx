import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  BarChart3, 
  Building2, 
  Settings,
  Globe,
  ChevronLeft,
  ChevronRight,
  BarChart
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  
  const menuItems = [
    { icon: BarChart3, label: 'Dashboard', path: '/dashboard' },
    { icon: Building2, label: 'Vendors', path: '/vendors' },
    { icon: BarChart, label: 'Chessboard', path: '/chessboard' },
    { icon: Settings, label: 'Settings', path: '/settings' },
  ];

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  return (
    <aside className={`${
      isCollapsed ? 'w-16' : 'w-64'
    } bg-transparent backdrop-blur-md border-r border-dark-700/50 flex flex-col relative z-50 transition-all duration-300 ease-in-out`}>
      {/* Logo */}
      <div className="px-6 py-4 border-b border-dark-700 relative">
        <div className="flex items-center gap-3">
          <Globe className="w-8 h-8 text-primary-500 flex-shrink-0" />
          {!isCollapsed && (
            <h1 className="text-xl font-bold text-white whitespace-nowrap">Runway Navigator</h1>
          )}
        </div>
        
        {/* Toggle Button */}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="absolute right-2 top-1/2 transform -translate-y-1/2 w-6 h-6 bg-dark-700 hover:bg-dark-600 rounded-full flex items-center justify-center text-dark-300 hover:text-white transition-all duration-200 border border-dark-600 z-10 shadow-lg hover:shadow-xl"
          title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {isCollapsed ? (
            <ChevronRight className="w-4 h-4" />
          ) : (
            <ChevronLeft className="w-4 h-4" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => (
            <li key={item.label}>
              <button
                onClick={() => handleNavigation(item.path)}
                className={`sidebar-item w-full text-left ${
                  location.pathname === item.path ? 'active' : ''
                }`}
                style={{
                  justifyContent: isCollapsed ? 'center' : 'flex-start',
                  paddingLeft: isCollapsed ? '0.5rem' : '1rem',
                  paddingRight: isCollapsed ? '0.5rem' : '1rem'
                }}
                title={isCollapsed ? item.label : undefined}
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                {!isCollapsed && (
                  <span className="whitespace-nowrap">{item.label}</span>
                )}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-dark-700">
        <div className="text-xs text-dark-400 text-center">
          {isCollapsed ? (
            <span title="v1.0.0 • Godmode Enabled">v1</span>
          ) : (
            <span>v1.0.0 • Godmode Enabled</span>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
