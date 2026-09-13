import { apiPostCsv } from "./client";

export async function exportPropensityCustomers() {
  const blob = await apiPostCsv("/api/v1/exports/propensity");
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "propensity_customers.csv";
  link.click();
  URL.revokeObjectURL(url);
}

