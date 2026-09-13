import { apiGet } from "./client";
import type { ChurnSummary } from "../types/churn";
import type { DashboardFilters } from "../types/portfolio";

function toQuery(filters: DashboardFilters) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value && value !== "All") params.set(key, value);
  });
  const query = params.toString();
  return query ? `?${query}` : "";
}

export function getChurnSummary(filters: DashboardFilters = {}) {
  return apiGet<ChurnSummary>(`/api/v1/churn/summary${toQuery(filters)}`);
}
