import React from 'react';

interface BadgeProps {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline';
  className?: string;
  children: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({ 
  variant = 'default', 
  className = '', 
  children 
}) => {
  const baseStyles = 'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors';
  
  const variants = {
    default: 'bg-primary-600/20 text-primary-400 border border-primary-600/30',
    secondary: 'bg-dark-700/50 text-dark-300 border border-dark-600/50',
    destructive: 'bg-red-600/20 text-red-400 border border-red-600/30',
    outline: 'border border-dark-600 text-dark-300 bg-transparent'
  };
  
  return (
    <span className={`${baseStyles} ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};
