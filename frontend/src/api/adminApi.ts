import { apiGet } from "./client";

export type KpiDefinition = {
  name: string;
  definition: string;
  module: string;
};

export type ApiDefinition = {
  method: string;
  path: string;
  description: string;
};

export function getKpiDefinitions() {
  return apiGet<KpiDefinition[]>("/api/v1/admin/kpis");
}

export function getApiDefinitions() {
  return apiGet<ApiDefinition[]>("/api/v1/admin/apis");
}

