import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './card';
import { Badge } from './badge';
import { Button } from './button';
import { 
  ChevronDown, 
  ChevronRight, 
  Info, 
  TrendingUp, 
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  XCircle
} from 'lucide-react';
import type { ChessboardNode, ChessboardBranch } from '../../lib/demo-store';

interface BaselineNode {
  cash: number;
  burn: number;
  runway: number;
}

interface MetricResult {
  value: number | string;
  delta?: number;
  p10?: number;
  p90?: number;
  confidence?: 'high' | 'medium' | 'low';
  sources?: string[];
}

interface MetricConfig {
  id: string;
  label: string;
  section: string;
  description: string;
  format: (value: number | string) => string;
  compute: (node: ChessboardNode | BaselineNode, baseline: BaselineNode) => MetricResult;
  thresholds?: {
    good: number;
    warning: number;
    critical: number;
  };
}

interface EnhancedCompareTableProps {
  baseline: BaselineNode;
  branches: ChessboardBranch[];
  onClose: () => void;
}

// Helper formatting functions
const formatCurrency = (amount: number) => {
  if (Math.abs(amount) >= 1000000) {
    return `$${(amount / 1000000).toFixed(1)}M`;
  }
  return `$${(amount / 1000).toFixed(0)}k`;
};

const formatPercentage = (value: number) => `${(value * 100).toFixed(1)}%`;
const formatMonths = (value: number) => `${value.toFixed(1)}m`;
const formatRatio = (value: number) => `${value.toFixed(1)}x`;
const formatNumber = (value: number) => value.toFixed(0);

// Simulate metrics with variance and confidence
const simulateMetrics = (node: ChessboardNode | BaselineNode, baseline: BaselineNode) => {
  const variance = (base: number, factor: number = 0.1) => ({
    p10: base * (1 - factor),
    p90: base * (1 + factor)
  });

  return {
    variance,
    confidence: Math.random() > 0.7 ? 'high' : Math.random() > 0.4 ? 'medium' : 'low' as const
  };
};

const METRICS_REGISTRY: MetricConfig[] = [
  {
    id: 'runway',
    label: 'Runway',
    section: 'Liquidity & Cash',
    description: 'Months of cash runway remaining at current burn rate',
    format: formatMonths,
    compute: (node, baseline) => {
      const { variance, confidence } = simulateMetrics(node, baseline);
      const runway = 'runway' in node ? node.runway : baseline.runway;
      const { p10, p90 } = variance(runway, 0.15);
      return {
        value: runway,
        delta: runway - baseline.runway,
        p10,
        p90,
        confidence,
        sources: ['Brex Cash', 'Bank APIs']
      };
    },
    thresholds: { good: 18, warning: 12, critical: 6 }
  },
  {
    id: 'burn',
    label: 'Monthly Burn',
    section: 'Liquidity & Cash',
    description: 'Monthly cash burn rate including all expenses',
    format: formatCurrency,
    compute: (node, baseline) => {
      const { variance, confidence } = simulateMetrics(node, baseline);
      const burn = 'monthlyBurn' in node ? node.monthlyBurn : baseline.burn;
      const { p10, p90 } = variance(burn, 0.08);
      return {
        value: burn,
        delta: burn - baseline.burn,
        p10,
        p90,
        confidence,
        sources: ['Brex Spend', 'Payroll APIs']
      };
    }
  },
  {
    id: 'mrr',
    label: 'Monthly Recurring Revenue',
    section: 'Growth & Revenue',
    description: 'Normalized monthly recurring revenue',
    format: formatCurrency,
    compute: (node, baseline) => {
      const burn = 'monthlyBurn' in node ? node.monthlyBurn : baseline.burn;
      const mrr = 95000 + (burn - baseline.burn) * 0.3;
      const { variance, confidence } = simulateMetrics(node, baseline);
      const { p10, p90 } = variance(mrr, 0.12);
      return {
        value: mrr,
        delta: mrr - 95000,
        p10,
        p90,
        confidence,
        sources: ['Stripe', 'ChartMogul']
      };
    }
  },
  {
    id: 'cac',
    label: 'Customer Acquisition Cost',
    section: 'Growth & Revenue',
    description: 'Blended customer acquisition cost across all channels',
    format: formatCurrency,
    compute: (node, baseline) => {
      const burn = 'monthlyBurn' in node ? node.monthlyBurn : baseline.burn;
      const cac = 2400 + (baseline.burn - burn) * 0.05;
      const { variance, confidence } = simulateMetrics(node, baseline);
      const { p10, p90 } = variance(cac, 0.20);
      return {
        value: cac,
        delta: cac - 2400,
        p10,
        p90,
        confidence,
        sources: ['MixRank', 'Facebook Ads']
      };
    },
    thresholds: { good: 2000, warning: 3000, critical: 4000 }
  },
  {
    id: 'ltv',
    label: 'Customer Lifetime Value',
    section: 'Growth & Revenue',
    description: 'Average customer lifetime value',
    format: formatCurrency,
    compute: (node, baseline) => {
      const runway = 'runway' in node ? node.runway : baseline.runway;
      const ltv = 28000 + (runway - baseline.runway) * 500;
      const { variance, confidence } = simulateMetrics(node, baseline);
      const { p10, p90 } = variance(ltv, 0.25);
      return {
        value: ltv,
        delta: ltv - 28000,
        p10,
        p90,
        confidence,
        sources: ['ChartMogul', 'Stripe']
      };
    }
  },
  {
    id: 'burnMultiple',
    label: 'Burn Multiple',
    section: 'Efficiency & Unit Economics',
    description: 'Net burn divided by net new ARR',
    format: formatRatio,
    compute: (node, baseline) => {
      const burn = 'monthlyBurn' in node ? node.monthlyBurn : baseline.burn;
      const multiple = burn / (95000 * 12 / 100) || 0;
      const { variance, confidence } = simulateMetrics(node, baseline);
      const { p10, p90 } = variance(multiple, 0.18);
      return {
        value: multiple,
        delta: multiple - (baseline.burn / (95000 * 12 / 100)),
        p10,
        p90,
        confidence,
        sources: ['Internal Analytics']
      };
    },
    thresholds: { good: 1.5, warning: 3.0, critical: 5.0 }
  },
  {
    id: 'nrr',
    label: 'Net Revenue Retention',
    section: 'Growth & Revenue',
    description: 'Net revenue retention rate from existing customers',
    format: formatPercentage,
    compute: (node, baseline) => {
      const runway = 'runway' in node ? node.runway : baseline.runway;
      const nrr = 1.15 + (runway - baseline.runway) * 0.005;
      const { variance, confidence } = simulateMetrics(node, baseline);
      const { p10, p90 } = variance(nrr, 0.08);
      return {
        value: nrr,
        delta: nrr - 1.15,
        p10,
        p90,
        confidence,
        sources: ['ChartMogul']
      };
    },
    thresholds: { good: 1.10, warning: 1.05, critical: 1.00 }
  },
  {
    id: 'fxImpact',
    label: 'FX Impact',
    section: 'Risk & Compliance',
    description: 'Foreign exchange impact on revenue',
    format: formatPercentage,
    compute: (node, baseline) => {
      const fx = -0.03 + (Math.random() - 0.5) * 0.04;
      const { confidence } = simulateMetrics(node, baseline);
      return {
        value: fx,
        delta: fx - (-0.03),
        confidence,
        sources: ['Currencies API']
      };
    }
  },
  {
    id: 'churn',
    label: 'Monthly Churn Rate',
    section: 'Growth & Revenue',
    description: 'Monthly customer churn rate',
    format: formatPercentage,
    compute: (node, baseline) => {
      const runway = 'runway' in node ? node.runway : baseline.runway;
      const churn = 0.035 - (runway - baseline.runway) * 0.0005;
      const { variance, confidence } = simulateMetrics(node, baseline);
      const { p10, p90 } = variance(churn, 0.25);
      return {
        value: churn,
        delta: churn - 0.035,
        p10,
        p90,
        confidence,
        sources: ['Internal CRM']
      };
    },
    thresholds: { good: 0.02, warning: 0.05, critical: 0.08 }
  }
];

const METRIC_SECTIONS = [
  'Liquidity & Cash',
  'Growth & Revenue', 
  'Efficiency & Unit Economics',
  'Risk & Compliance'
];

export const EnhancedCompareTable = ({ baseline, branches, onClose }: EnhancedCompareTableProps) => {
  const [expandedSections, setExpandedSections] = useState(
    new Set(['Liquidity & Cash', 'Growth & Revenue']) // Start with key sections expanded
  );

  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

  const getMetricsBySection = (section: string): MetricConfig[] => {
    return METRICS_REGISTRY.filter(metric => metric.section === section);
  };

  const getThresholdColor = (value: number | string, metric: MetricConfig) => {
    if (!metric.thresholds || typeof value !== 'number') return '';

    const { good, warning, critical } = metric.thresholds;

    // For metrics where higher is better
    if (metric.id === 'runway' || metric.id === 'grossMargin' || metric.id === 'nrr') {
      if (value >= good) return 'text-green-600';
      if (value >= warning) return 'text-yellow-600';
      return 'text-red-600';
    }

    // For metrics where lower is better  
    if (metric.id === 'burnMultiple' || metric.id === 'churn' || metric.id === 'payback') {
      if (value <= good) return 'text-green-600';
      if (value <= warning) return 'text-yellow-600';
      return 'text-red-600';
    }

    return '';
  };

  const getThresholdIcon = (value: number | string, metric: MetricConfig) => {
    if (!metric.thresholds || typeof value !== 'number') return null;

    const { good, warning, critical } = metric.thresholds;
    const isHigherBetter = ['runway', 'grossMargin', 'nrr'].includes(metric.id);
    const isLowerBetter = ['burnMultiple', 'churn', 'payback'].includes(metric.id);

    let status: 'good' | 'warning' | 'critical';

    if (isHigherBetter) {
      status = value >= good ? 'good' : value >= warning ? 'warning' : 'critical';
    } else if (isLowerBetter) {
      status = value <= good ? 'good' : value <= warning ? 'warning' : 'critical';
    } else {
      return null;
    }

    switch (status) {
      case 'good':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-600" />;
      case 'critical':
        return <XCircle className="w-4 h-4 text-red-600" />;
    }
  };

  const getDeltaDisplay = (delta: number | undefined, format: (value: number | string) => string) => {
    if (delta === undefined || Math.abs(delta) < 0.01) return null;

    const isPositive = delta > 0;
    const Icon = isPositive ? TrendingUp : TrendingDown;
    const colorClass = isPositive ? 'text-green-600' : 'text-red-600';

    return (
      <div className={`flex items-center gap-1 text-xs ${colorClass}`}>
        <Icon className="w-3 h-3" />
        {isPositive ? '+' : ''}{format(delta)}
      </div>
    );
  };

  const getBranchColor = (branchId: string) => {
    switch (branchId) {
      case 'A': return 'bg-primary-600 text-white';
      case 'B': return 'bg-green-600 text-white';  
      case 'C': return 'bg-purple-600 text-white';
      case 'D': return 'bg-orange-600 text-white';
      default: return 'bg-dark-700 text-white';
    }
  };

  const getConfidenceColor = (confidence: 'high' | 'medium' | 'low' | undefined) => {
    switch (confidence) {
      case 'high': return 'text-green-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-red-600';
      default: return 'text-dark-400';
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-7xl max-h-[90vh] overflow-auto">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">KPI Comparison Analysis</CardTitle>
              <p className="text-dark-300 mt-2">
                Comparing baseline scenario with {branches.length} branch scenarios across {METRIC_SECTIONS.length} metric categories
              </p>
            </div>
            <Button onClick={onClose} variant="outline">
              Exit Compare
            </Button>
          </div>
        </CardHeader>

        <CardContent>
          {METRIC_SECTIONS.map((section) => {
            const metrics = getMetricsBySection(section);
            const isExpanded = expandedSections.has(section);

            return (
              <div key={section} className="mb-6">
                <button
                  onClick={() => toggleSection(section)}
                  className="flex items-center gap-3 w-full text-left p-3 rounded-lg hover:bg-dark-800/50 transition-colors"
                >
                  {isExpanded ? <ChevronDown className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
                  <h3 className="text-lg font-semibold">{section}</h3>
                  <Badge variant="outline">
                    {metrics.length} metrics
                  </Badge>
                </button>

                {isExpanded && (
                  <div className="ml-8 mt-3">
                    <div className="overflow-x-auto">
                      <table className="w-full border-collapse">
                        <thead>
                          <tr className="border-b border-dark-700">
                            <th className="text-left p-3 font-medium text-dark-300">
                              Metric
                            </th>
                            <th className="text-center p-3 font-medium text-dark-300">
                              Baseline
                            </th>
                            {branches.map(branch => (
                              <th key={branch.id} className="text-center p-3 font-medium text-dark-300">
                                <div className="flex flex-col items-center gap-1">
                                  <span>Branch {branch.id}</span>
                                  <Badge className={getBranchColor(branch.id)}>
                                    {branch.id}
                                  </Badge>
                                </div>
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {metrics.map((metric) => {
                            const baselineData = metric.compute(baseline, baseline);

                            return (
                              <tr key={metric.id} className="border-b border-dark-700/50 hover:bg-dark-800/30">
                                <td className="p-3">
                                  <div className="flex items-center gap-2">
                                    <span className="font-medium">{metric.label}</span>
                                    <div className="group relative">
                                      <Info className="w-4 h-4 text-dark-400 cursor-help" />
                                      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-dark-800 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                                        {metric.description}
                                        {baselineData.sources && (
                                          <div className="mt-2 pt-2 border-t border-dark-600">
                                            <div className="text-xs text-dark-300 mb-1">Sources:</div>
                                            {baselineData.sources.map((source, i) => (
                                              <div key={i} className="text-xs text-dark-400">
                                                • {source}
                                              </div>
                                            ))}
                                          </div>
                                        )}
                                      </div>
                                    </div>
                                  </div>
                                </td>

                                {/* Baseline column */}
                                <td className="p-3 text-center">
                                  <div className="flex flex-col items-center gap-1">
                                    <span className={`font-semibold ${getThresholdColor(baselineData.value, metric)}`}>
                                      {metric.format(baselineData.value)}
                                    </span>
                                    {getThresholdIcon(baselineData.value, metric)}
                                    
                                    {baselineData.p10 !== undefined && baselineData.p90 !== undefined && (
                                      <div className="text-xs text-dark-400">
                                        {metric.format(baselineData.p10)} - {metric.format(baselineData.p90)}
                                      </div>
                                    )}
                                    
                                    {baselineData.confidence && (
                                      <Badge variant="outline" className={`text-xs ${getConfidenceColor(baselineData.confidence)}`}>
                                        {baselineData.confidence} confidence
                                      </Badge>
                                    )}
                                  </div>
                                </td>

                                {/* Branch columns */}
                                {branches.map(branch => {
                                  const finalNode = branch.nodes[branch.nodes.length - 1] || baseline;
                                  const branchData = metric.compute(finalNode, baseline);

                                  return (
                                    <td key={branch.id} className="p-3 text-center">
                                      <div className="flex flex-col items-center gap-1">
                                        <span className={`font-semibold ${getThresholdColor(branchData.value, metric)}`}>
                                          {metric.format(branchData.value)}
                                        </span>
                                        {getThresholdIcon(branchData.value, metric)}
                                        
                                        {branchData.p10 !== undefined && branchData.p90 !== undefined && (
                                          <div className="text-xs text-dark-400">
                                            {metric.format(branchData.p10)} - {metric.format(branchData.p90)}
                                          </div>
                                        )}
                                        
                                        {getDeltaDisplay(branchData.delta, metric.format)}
                                        
                                        {branchData.confidence && (
                                          <Badge variant="outline" className={`text-xs ${getConfidenceColor(branchData.confidence)}`}>
                                            {branchData.confidence}
                                          </Badge>
                                        )}
                                      </div>
                                    </td>
                                  );
                                })}
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </CardContent>
      </Card>
    </div>
  );
};
