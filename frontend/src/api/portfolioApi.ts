import { apiGet } from "./client";
import type { DashboardFilters, PortfolioSummary, SegmentOptions } from "../types/portfolio";

function toQuery(filters: DashboardFilters) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value && value !== "All") params.set(key, value);
  });
  const query = params.toString();
  return query ? `?${query}` : "";
}

export function getPortfolioSummary(filters: DashboardFilters = {}) {
  return apiGet<PortfolioSummary>(`/api/v1/portfolio/summary${toQuery(filters)}`);
}

export function getPortfolioSegments() {
  return apiGet<SegmentOptions>("/api/v1/portfolio/segments");
}
