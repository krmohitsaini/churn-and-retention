import { Navigate, Route, Routes } from "react-router-dom";

import { AdminApiPage } from "./pages/AdminApiPage";
import { AdminKpiPage } from "./pages/AdminKpiPage";
import { ChurnPage } from "./pages/ChurnPage";
import { CustomerDetailPage } from "./pages/CustomerDetailPage";
import { PortfolioPage } from "./pages/PortfolioPage";
import { PropensityPage } from "./pages/PropensityPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/portfolio" replace />} />
      <Route path="/portfolio" element={<PortfolioPage />} />
      <Route path="/churn" element={<ChurnPage />} />
      <Route path="/propensity" element={<PropensityPage />} />
      <Route path="/customers/:customerId" element={<CustomerDetailPage />} />
      <Route path="/admin/kpis" element={<AdminKpiPage />} />
      <Route path="/admin/apis" element={<AdminApiPage />} />
    </Routes>
  );
}

