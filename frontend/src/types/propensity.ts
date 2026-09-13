import type { MetricCard } from "./portfolio";

export type ChurnDriver = {
  driver: string | null;
  weight: number | null;
};

export type PropensityCustomer = {
  customer_id: string;
  customer_name?: string;
  province?: string;
  segment?: string;
  product_type?: string;
  tenure_months?: number;
  estimated_annual_value?: number;
  churn_probability: number;
  risk_band: string;
  prediction_window_days: number;
  top_driver?: string;
  recommended_action?: string;
  recommended_offer?: string;
  drivers: ChurnDriver[];
};

export type PropensitySummary = {
  metrics: MetricCard[];
  customers: PropensityCustomer[];
};

