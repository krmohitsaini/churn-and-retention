import type { ChartPoint, MetricCard } from "./portfolio";

export type ChurnTimeseriesPoint = {
  month: string;
  churned_sites: number;
};

export type ChurnSummary = {
  metrics: MetricCard[];
  timeseries: ChurnTimeseriesPoint[];
  outcomes: ChartPoint[];
  by_commodity: ChartPoint[];
  by_channel: ChartPoint[];
  by_sales_type: ChartPoint[];
  by_billing: ChartPoint[];
  by_digital: ChartPoint[];
  by_agent: ChartPoint[];
  monthly_outcomes: MonthlyOutcomePoint[];
};

export type MonthlyOutcomePoint = {
  month: string;
  Churn: number;
  "Auto Renewal": number;
  "Positive Renewal": number;
  TOS: number;
  Leakage: number;
};
