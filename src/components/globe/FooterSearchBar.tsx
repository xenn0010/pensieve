import React, { useState } from 'react';
import { Search, X } from 'lucide-react';

interface FooterSearchBarProps {
  onSearch: (query: string) => void;
  onClear?: () => void;
  hasResults?: boolean;
  placeholder?: string;
}

const FooterSearchBar: React.FC<FooterSearchBarProps> = ({ 
  onSearch, 
  onClear,
  hasResults = false,
  placeholder = "Search companies, locations, or risk levels..." 
}) => {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
      setQuery('');
    }
  };

  const handleClear = () => {
    setQuery('');
  };

  return (
    <div className="absolute bottom-24 left-1/2 transform -translate-x-1/2 w-96 max-w-[90vw] z-30">
      <form onSubmit={handleSubmit} className="relative">
        <div className={`
          relative flex items-center bg-dark-800/20 backdrop-blur-md 
          border border-dark-700/50 rounded-xl shadow-xl 
          transition-all duration-300 overflow-hidden
          ${isFocused ? 'border-primary-500/50 shadow-primary-500/25' : 'hover:border-dark-600/50'}
        `}>
          {/* Search Icon */}
          <div className="pl-4 pr-3">
            <Search className="w-5 h-5 text-dark-400" />
          </div>
          
          {/* Search Input */}
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder={placeholder}
            className="flex-1 bg-transparent text-white placeholder-dark-400 
                     py-4 px-2 outline-none text-sm"
          />
          
          {/* Clear Button */}
          {query && (
            <button
              type="button"
              onClick={handleClear}
              className="p-2 hover:bg-dark-700/50 rounded-lg transition-colors mr-2"
            >
              <X className="w-4 h-4 text-dark-400 hover:text-white" />
            </button>
          )}
          
          {/* Search Button */}
          <button
            type="submit"
            disabled={!query.trim()}
            className={`
              px-4 py-4 bg-primary-600/90 hover:bg-primary-600 
              disabled:bg-dark-700/50 disabled:cursor-not-allowed
              text-white font-medium transition-all duration-200
              ${query.trim() ? 'hover:shadow-lg hover:shadow-primary-500/25' : ''}
            `}
          >
            Search
          </button>
        </div>
      </form>
      
      {/* Clear Results Button - Shows when there are search results */}
      {hasResults && onClear && (
        <div className="mt-3 flex justify-center">
          <button
            onClick={onClear}
            className="px-4 py-2 bg-dark-700/60 hover:bg-dark-600/60 text-dark-300 hover:text-white 
                     rounded-lg transition-all duration-200 text-sm backdrop-blur-md border border-dark-600/50"
          >
            Clear Search Results
          </button>
        </div>
      )}
    </div>
  );
};

export default FooterSearchBar;
