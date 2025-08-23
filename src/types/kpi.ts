export interface KPI {
  label: string;
  value: string | number;
  change?: number;
  trend: 'up' | 'down' | 'stable';
  unit: string;
  description?: string;
  icon?: string;
  color?: string;
}
