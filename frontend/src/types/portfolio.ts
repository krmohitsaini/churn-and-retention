export type MetricCard = {
  label: string;
  value: string | number;
  helper?: string | null;
};

export type ChartPoint = {
  name: string;
  value: number;
};

export type PortfolioSummary = {
  metrics: MetricCard[];
  by_commodity: ChartPoint[];
  by_channel: ChartPoint[];
  by_sales_type: ChartPoint[];
  by_billing: ChartPoint[];
  by_evergreen: ChartPoint[];
  by_surge: ChartPoint[];
  signups_by_month: SignupPoint[];
  active_contract_starts: ActiveContractStartPoint[];
  site_density: ChartPoint[];
};

export type SegmentOptions = Record<string, string[]>;

export type DashboardFilters = {
  commodity_type?: string;
  channel?: string;
  sales_type?: string;
  AMB_status?: string;
  evergreen_status?: string;
  surge_status?: string;
  digital_status?: string;
  dob_status?: string;
};

export type SignupPoint = {
  month: string;
  signed_up_customers: number;
};

export type ActiveContractStartPoint = {
  month: string;
  active_contract_starts: number;
};
