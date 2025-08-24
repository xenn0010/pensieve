import React, { useEffect, useState } from 'react';
import { Clock, TrendingUp, TrendingDown, Minus, DollarSign, CreditCard, Building2 } from 'lucide-react';
import { API_CONFIG } from '../../config/api';
import { FinancialTransaction, FinancialSummary } from '../../types/financial';

const TransactionOverlay: React.FC = () => {
  const [transactions, setTransactions] = useState<FinancialTransaction[]>([]);
  const [summary, setSummary] = useState<FinancialSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch financial transactions from API
  const fetchFinancialTransactions = async () => {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.FINANCIAL_TRANSACTIONS}`);
      if (!response.ok) {
        throw new Error('Failed to fetch financial transactions');
      }
      
      const data = await response.json();
      setTransactions(data.transactions);
      setSummary(data.summary);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching financial transactions:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      setLoading(false);
      
      // Fallback to empty state
      setTransactions([]);
      setSummary(null);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchFinancialTransactions();
    
    // Refresh data every 60 seconds
    const interval = setInterval(fetchFinancialTransactions, 60000);
    
    return () => clearInterval(interval);
  }, []);

  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'revenue':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'expense':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      case 'payroll':
        return <CreditCard className="w-4 h-4 text-blue-500" />;
      case 'vendor':
        return <Building2 className="w-4 h-4 text-yellow-500" />;
      default:
        return <DollarSign className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500';
      case 'pending':
        return 'bg-yellow-500';
      case 'failed':
        return 'bg-red-500';
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
          <DollarSign className="w-5 h-5 text-green-500" />
          <h3 className="text-lg font-semibold text-white">Company Finances</h3>
        </div>
        <p className="text-sm text-dark-300 mt-1">
          Recent financial transactions and cash flow
        </p>
        
        {/* Financial Summary */}
        {summary && (
          <div className="mt-3 p-3 bg-dark-700/30 rounded-lg">
            <div className="grid grid-cols-3 gap-4 text-xs">
              <div className="text-center">
                <div className="text-green-400 font-semibold">+${(summary.total_revenue / 1000).toFixed(0)}K</div>
                <div className="text-dark-400">Revenue</div>
              </div>
              <div className="text-center">
                <div className="text-red-400 font-semibold">-${(summary.total_expenses / 1000).toFixed(0)}K</div>
                <div className="text-dark-400">Expenses</div>
              </div>
              <div className="text-center">
                <div className={`font-semibold ${summary.net_cash_flow >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {summary.net_cash_flow >= 0 ? '+' : ''}${(summary.net_cash_flow / 1000).toFixed(0)}K
                </div>
                <div className="text-dark-400">Net Flow</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Transactions List - Seamlessly connected to header */}
      <div className="max-h-80 overflow-y-auto bg-dark-800/30 rounded-b-xl">
        {loading ? (
          // Loading state
          <div className="p-4 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500 mx-auto mb-2"></div>
            <p className="text-dark-300 text-sm">Loading financial data...</p>
          </div>
        ) : error ? (
          // Error state
          <div className="p-4 text-center">
            <p className="text-red-400 text-sm mb-2">⚠️ Error loading data</p>
            <p className="text-dark-300 text-xs">{error}</p>
          </div>
        ) : transactions.length === 0 ? (
          // Empty state
          <div className="p-4 text-center">
            <p className="text-dark-300 text-sm">No financial transactions found</p>
          </div>
        ) : (
          // Transactions list
          transactions.map((transaction, index) => (
            <div
              key={transaction.id}
              className={`p-4 transition-colors cursor-pointer hover:bg-dark-700/30 ${
                index === transactions.length - 1 ? '' : 'border-b border-dark-700/30'
              }`}
            >
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 mt-1">
                  {getTransactionIcon(transaction.type)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="text-sm font-medium text-white truncate">
                      {transaction.merchant}
                    </h4>
                    <span className={`inline-block w-2 h-2 rounded-full ${getStatusColor(transaction.status)}`} />
                  </div>
                  
                  <p className="text-xs text-dark-300 mb-2 line-clamp-2">
                    {transaction.description}
                  </p>
                  
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-dark-400 capitalize">
                      {transaction.category}
                    </span>
                    <span className="text-dark-400">
                      {formatTimestamp(new Date(transaction.timestamp))}
                    </span>
                  </div>
                  
                  <div className="mt-2 text-sm font-medium text-primary-400">
                    {formatAmount(Math.abs(transaction.amount), transaction.currency)}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="p-3 bg-dark-800/50 border-t border-dark-700">
        <div className="text-xs text-dark-400 text-center">
          {transactions.length} financial transactions • Updated in real-time
        </div>
      </div>
    </div>
  );
};

export default TransactionOverlay;
