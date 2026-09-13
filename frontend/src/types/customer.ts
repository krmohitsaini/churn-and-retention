export type CustomerDetail = {
  customer: Record<string, string | number | boolean | null>;
  propensity?: Record<string, string | number | boolean | null>;
  interactions: Record<string, string | number | boolean | null>[];
};

