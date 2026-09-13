import { apiGet } from "./client";
import type { CustomerDetail } from "../types/customer";

export function getCustomerDetail(customerId: string) {
  return apiGet<CustomerDetail>(`/api/v1/customers/${customerId}`);
}

