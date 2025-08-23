import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  DollarSign,
  Calendar,
  Target
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import type { ChessboardNode, ChessboardBranch } from '../../lib/demo-store';

interface BaselineNode {
  cash: number;
  burn: number;
  runway: number;
}

interface VisualCompareChartProps {
  baseline: BaselineNode;
  branches: ChessboardBranch[];
  onClose: () => void;
}

export const VisualCompareChart = ({ baseline, branches, onClose }: VisualCompareChartProps) => {
  const [selectedMetric, setSelectedMetric] = useState<'runway' | 'burn' | 'cash'>('runway');
  const [chartType, setChartType] = useState<'bar' | 'line' | 'pie'>('bar');

  const getMetricData = () => {
    // Ensure we have valid baseline values
    const baselineValue = baseline[selectedMetric] || 0;
    
    const branchData = branches.map(branch => {
      const finalNode = branch.nodes[branch.nodes.length - 1];
      if (!finalNode) return { id: branch.id, value: baselineValue, delta: 0, name: branch.name };
      
      let value: number;
      if (selectedMetric === 'runway') {
        value = finalNode.runway || 0;
      } else if (selectedMetric === 'burn') {
        value = finalNode.monthlyBurn || 0;
      } else if (selectedMetric === 'cash') {
        value = finalNode.cashInjection || 0;
      } else {
        value = 0;
      }
      
      return {
        id: branch.id,
        value,
        delta: value - baselineValue,
        name: branch.name
      };
    });

    // Always include baseline, even if no branches
    const result = [
      { id: 'baseline', value: baselineValue, delta: 0, name: 'Baseline' },
      ...branchData
    ];
    
    return result;
  };

  const getMetricLabel = () => {
    switch (selectedMetric) {
      case 'runway': return 'Runway (months)';
      case 'burn': return 'Monthly Burn ($)';
      case 'cash': return 'Cash Injection ($)';
      default: return '';
    }
  };

  const getMetricIcon = () => {
    switch (selectedMetric) {
      case 'runway': return <Calendar className="w-5 h-5" />;
      case 'burn': return <DollarSign className="w-5 h-5" />;
      case 'cash': return <Target className="w-5 h-5" />;
      default: return null;
    }
  };

  const formatValue = (value: number) => {
    switch (selectedMetric) {
      case 'runway': return `${value.toFixed(1)}m`;
      case 'burn': return value >= 1000000 ? `$${(value / 1000000).toFixed(1)}M` : `$${(value / 1000).toFixed(0)}k`;
      case 'cash': return value >= 1000000 ? `$${(value / 1000000).toFixed(1)}M` : `$${(value / 1000).toFixed(0)}k`;
      default: return value.toString();
    }
  };



  const getBarColor = (id: string, delta: number) => {
    if (id === 'baseline') return '#3B82F6'; // Blue
    if (delta > 0) return '#10B981'; // Green
    if (delta < 0) return '#EF4444'; // Red
    return '#6B7280'; // Gray
  };

  const getDeltaIcon = (delta: number) => {
    if (delta > 0) return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (delta < 0) return <TrendingDown className="w-4 h-4 text-red-500" />;
    return null;
  };

  const getDeltaColor = (delta: number) => {
    if (delta > 0) return 'text-green-500';
    if (delta < 0) return 'text-red-500';
    return 'text-gray-500';
  };

  // Get data inside the render function to ensure it updates
  const data = getMetricData();

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-6xl max-h-[90vh] overflow-auto">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <BarChart3 className="w-6 h-6 text-primary-500" />
              <div>
                <CardTitle className="text-2xl">Visual Scenario Comparison</CardTitle>
                <p className="text-dark-300 mt-1">
                  Visual comparison of {branches.length} scenarios vs baseline
                </p>
              </div>
            </div>
            <Button onClick={onClose} variant="outline">
              Exit Visual Compare
            </Button>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Metric Selector */}
          <div className="flex items-center gap-4 p-4 bg-dark-800/50 rounded-lg border border-dark-700">
            <div className="flex items-center gap-2">
              {getMetricIcon()}
              <span className="font-medium">Compare by:</span>
            </div>
            
            <div className="flex gap-2">
              {[
                { key: 'runway', label: 'Runway' },
                { key: 'burn', label: 'Monthly Burn' },
                { key: 'cash', label: 'Cash Injection' }
              ].map(metric => (
                <Button
                  key={metric.key}
                  variant={selectedMetric === metric.key ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedMetric(metric.key as any)}
                >
                  {metric.label}
                </Button>
              ))}
            </div>
          </div>

          {/* Chart Type Toggle */}
          <div className="flex items-center gap-4">
            <span className="font-medium">Chart Type:</span>
            <div className="flex gap-2">
              <Button
                variant={chartType === 'bar' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setChartType('bar')}
              >
                Bar Chart
              </Button>
              <Button
                variant={chartType === 'line' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setChartType('line')}
              >
                Line Chart
              </Button>
              <Button
                variant={chartType === 'pie' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setChartType('pie')}
              >
                Pie Chart
              </Button>
            </div>
          </div>

          {/* Chart Display */}
          <div className="bg-dark-800/30 rounded-lg p-6 border border-dark-700 backdrop-blur-sm">
            <div className="text-center mb-6">
              <div className="flex items-center justify-center gap-2 mb-2">
                {getMetricIcon()}
                <h3 className="text-xl font-semibold">{getMetricLabel()}</h3>
              </div>
              <p className="text-dark-300 text-sm">
                {selectedMetric === 'runway' ? 'Higher is better' : 
                 selectedMetric === 'burn' ? 'Lower is better' : 
                 'Higher is better'}
              </p>
            </div>
            


            {chartType === 'bar' ? (
              /* Professional Bar Chart */
              <div className="h-80 w-full">
                {data && data.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={data}
                      margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                      className="text-white"
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                      <XAxis 
                        dataKey="name" 
                        tick={{ fill: '#9CA3AF' }}
                        tickLine={{ stroke: '#4B5563' }}
                        axisLine={{ stroke: '#4B5563' }}
                      />
                      <YAxis 
                        tick={{ fill: '#9CA3AF' }}
                        tickLine={{ stroke: '#4B5563' }}
                        axisLine={{ stroke: '#4B5563' }}
                        tickFormatter={(value) => formatValue(value)}
                      />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '8px',
                          color: 'white'
                        }}
                        formatter={(value: any) => [formatValue(value), getMetricLabel()]}
                        labelStyle={{ color: '#9CA3AF' }}
                      />
                      <Bar 
                        dataKey="value" 
                        radius={[4, 4, 0, 0]}
                        fill="#3B82F6"
                      >
                        {data.map((entry, index) => (
                          <Cell 
                            key={`cell-${index}`}
                            fill={getBarColor(entry.id, entry.delta)}
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="text-center text-dark-400 h-full flex items-center justify-center">
                    <div>
                      <BarChart3 className="w-16 h-16 mx-auto mb-4 opacity-30" />
                      <p>No data available for comparison</p>
                      <p className="text-sm">Create some scenarios first</p>
                    </div>
                  </div>
                )}
              </div>
            ) : chartType === 'line' ? (
              /* Professional Line Chart */
              <div className="h-80 w-full">
                {data && data.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                      data={data}
                      margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                      className="text-white"
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                      <XAxis 
                        dataKey="name" 
                        tick={{ fill: '#9CA3AF' }}
                        tickLine={{ stroke: '#4B5563' }}
                        axisLine={{ stroke: '#4B5563' }}
                      />
                      <YAxis 
                        tick={{ fill: '#9CA3AF' }}
                        tickLine={{ stroke: '#4B5563' }}
                        axisLine={{ stroke: '#4B5563' }}
                        tickFormatter={(value) => formatValue(value)}
                      />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '8px',
                          color: 'white'
                        }}
                        formatter={(value: any) => [formatValue(value), getMetricLabel()]}
                        labelStyle={{ color: '#9CA3AF' }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="value" 
                        stroke="#3B82F6" 
                        strokeWidth={3}
                        dot={{ fill: '#3B82F6', strokeWidth: 2, r: 6 }}
                        activeDot={{ r: 8, stroke: '#3B82F6', strokeWidth: 2, fill: '#1F2937' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="text-center text-dark-400 h-full flex items-center justify-center">
                    <div>
                      <BarChart3 className="w-16 h-16 mx-auto mb-4 opacity-30" />
                      <p>No data available for comparison</p>
                      <p className="text-sm">Create some scenarios first</p>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              /* Professional Pie Chart */
              <div className="h-80 w-full">
                {data && data.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                        outerRadius={120}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {data.map((entry, index) => (
                          <Cell 
                            key={`cell-${index}`}
                            fill={getBarColor(entry.id, entry.delta)}
                          />
                        ))}
                      </Pie>
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '8px',
                          color: 'white'
                        }}
                        formatter={(value: any) => [formatValue(value), getMetricLabel()]}
                        labelStyle={{ color: '#9CA3AF' }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="text-center text-dark-400 h-full flex items-center justify-center">
                    <div>
                      <BarChart3 className="w-16 h-16 mx-auto mb-4 opacity-30" />
                      <p>No data available for comparison</p>
                      <p className="text-sm">Create some scenarios first</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Summary Table */}
          <div className="bg-dark-800/30 rounded-lg border border-dark-700 overflow-hidden">
            <div className="p-4 border-b border-dark-700">
              <h4 className="font-semibold">Scenario Summary</h4>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-dark-800/50">
                  <tr>
                    <th className="text-left p-3 font-medium text-dark-300">Scenario</th>
                    <th className="text-center p-3 font-medium text-dark-300">Value</th>
                    <th className="text-center p-3 font-medium text-dark-300">Change</th>
                    <th className="text-center p-3 font-medium text-dark-300">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((item, index) => (
                    <tr key={item.id} className="border-b border-dark-700/50 hover:bg-dark-800/30">
                      <td className="p-3">
                        <div className="flex items-center gap-3">
                          {item.id === 'baseline' ? (
                            <div className="w-3 h-3 bg-blue-600 rounded-full" />
                          ) : (
                            <div className={`w-3 h-3 rounded-full ${item.delta > 0 ? 'bg-green-600' : item.delta < 0 ? 'bg-red-600' : 'bg-gray-600'}`} />
                          )}
                          <span className="font-medium">{item.name}</span>
                        </div>
                      </td>
                      <td className="p-3 text-center font-semibold">
                        {formatValue(item.value)}
                      </td>
                      <td className="p-3 text-center">
                        {item.id === 'baseline' ? (
                          <span className="text-dark-400">—</span>
                        ) : (
                          <div className={`flex items-center justify-center gap-1 ${getDeltaColor(item.delta)}`}>
                            {getDeltaIcon(item.delta)}
                            <span>{item.delta > 0 ? '+' : ''}{formatValue(Math.abs(item.delta))}</span>
                          </div>
                        )}
                      </td>
                      <td className="p-3 text-center">
                        {item.id === 'baseline' ? (
                          <Badge variant="secondary">Baseline</Badge>
                        ) : (
                          <Badge variant={item.delta > 0 ? 'default' : item.delta < 0 ? 'destructive' : 'outline'}>
                            {item.delta > 0 ? 'Improved' : item.delta < 0 ? 'Declined' : 'No Change'}
                          </Badge>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Insights */}
          <div className="bg-dark-800/30 rounded-lg p-4 border border-dark-700">
            <h4 className="font-semibold mb-3">Key Insights</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-dark-400">Best Scenario: </span>
                <span className="font-medium text-green-400">
                  {data.filter(d => d.id !== 'baseline').reduce((best, current) => 
                    selectedMetric === 'burn' ? 
                      (current.value < best.value ? current : best) : 
                      (current.value > best.value ? current : best)
                  ).name}
                </span>
              </div>
              <div>
                <span className="text-dark-400">Worst Scenario: </span>
                <span className="font-medium text-red-400">
                  {data.filter(d => d.id !== 'baseline').reduce((worst, current) => 
                    selectedMetric === 'burn' ? 
                      (current.value > worst.value ? current : worst) : 
                      (current.value < worst.value ? current : worst)
                  ).name}
                </span>
              </div>
              <div>
                <span className="text-dark-400">Average Change: </span>
                <span className="font-medium">
                  {(() => {
                    const changes = data.filter(d => d.id !== 'baseline').map(d => d.delta);
                    const avg = changes.reduce((sum, change) => sum + change, 0) / changes.length;
                    return (
                      <span className={getDeltaColor(avg)}>
                        {avg > 0 ? '+' : ''}{formatValue(Math.abs(avg))}
                      </span>
                    );
                  })()}
                </span>
              </div>
              <div>
                <span className="text-dark-400">Scenarios Analyzed: </span>
                <span className="font-medium text-white">{branches.length}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
