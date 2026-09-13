import { apiGet } from "./client";
import type { PropensityCustomer, PropensitySummary } from "../types/propensity";

export function getPropensitySummary() {
  return apiGet<PropensitySummary>("/api/v1/propensity/summary");
}

export function getPropensityCustomer(customerId: string) {
  return apiGet<PropensityCustomer>(`/api/v1/propensity/customers/${customerId}`);
}

