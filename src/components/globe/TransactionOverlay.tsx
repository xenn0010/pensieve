import React from 'react';
import { Clock, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { mockTransactions } from '../../data/mockTransactions';

const TransactionOverlay: React.FC = () => {
  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'funding':
      case 'investment':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'acquisition':
      case 'merger':
        return <TrendingDown className="w-4 h-4 text-blue-500" />;
      default:
        return <Minus className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500';
      case 'pending':
        return 'bg-yellow-500';
      case 'cancelled':
        return 'bg-red-500';
      case 'announced':
        return 'bg-blue-500';
      default:
        return 'bg-gray-500';
    }
  };

  const formatAmount = (amount?: number, currency?: string) => {
    if (!amount) return 'N/A';
    
    const formatter = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency || 'USD',
      notation: 'compact',
      maximumFractionDigits: 1,
    });
    
    return formatter.format(amount);
  };

  const formatTimestamp = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    
    if (days > 0) {
      return `${days} day${days > 1 ? 's' : ''} ago`;
    } else if (hours > 0) {
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
      return 'Just now';
    }
  };

  return (
    <div className="absolute left-6 top-40 w-80 max-h-[calc(100vh-10rem)] bg-dark-800/95 backdrop-blur-md rounded-xl border border-dark-700 shadow-2xl overflow-hidden z-30">
      {/* Header - Connected seamlessly to content */}
      <div className="p-4 bg-dark-800/50 rounded-t-xl">
        <div className="flex items-center gap-3">
          <Clock className="w-5 h-5 text-primary-500" />
          <h3 className="text-lg font-semibold text-white">Recent Transactions</h3>
        </div>
        <p className="text-sm text-dark-300 mt-1">
          Latest market activity and deals
        </p>
      </div>

      {/* Transactions List - Seamlessly connected to header */}
      <div className="max-h-80 overflow-y-auto bg-dark-800/30 rounded-b-xl">
        {mockTransactions.map((transaction, index) => (
          <div
            key={transaction.id}
            className={`p-4 transition-colors cursor-pointer hover:bg-dark-700/30 ${
              index === mockTransactions.length - 1 ? '' : 'border-b border-dark-700/30'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 mt-1">
                {getTransactionIcon(transaction.type)}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="text-sm font-medium text-white truncate">
                    {transaction.companyName}
                  </h4>
                  <span className={`inline-block w-2 h-2 rounded-full ${getStatusColor(transaction.status)}`} />
                </div>
                
                <p className="text-xs text-dark-300 mb-2 line-clamp-2">
                  {transaction.description}
                </p>
                
                <div className="flex items-center justify-between text-xs">
                  <span className="text-dark-400 capitalize">
                    {transaction.type.replace('_', ' ')}
                  </span>
                  <span className="text-dark-400">
                    {formatTimestamp(transaction.timestamp)}
                  </span>
                </div>
                
                {transaction.amount && (
                  <div className="mt-2 text-sm font-medium text-primary-400">
                    {formatAmount(transaction.amount, transaction.currency)}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="p-3 bg-dark-800/50 border-t border-dark-700">
        <div className="text-xs text-dark-400 text-center">
          {mockTransactions.length} transactions • Updated in real-time
        </div>
      </div>
    </div>
  );
};

export default TransactionOverlay;
