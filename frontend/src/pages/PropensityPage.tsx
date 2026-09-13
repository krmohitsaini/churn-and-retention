import { Download } from "lucide-react";
import { useEffect, useState } from "react";

import { exportPropensityCustomers } from "../api/exportApi";
import { getPropensitySummary } from "../api/propensityApi";
import { KpiCard } from "../components/cards/KpiCard";
import { ErrorState } from "../components/states/ErrorState";
import { LoadingState } from "../components/states/LoadingState";
import { PropensityTable } from "../components/tables/PropensityTable";
import type { PropensitySummary } from "../types/propensity";

export function PropensityPage() {
  const [data, setData] = useState<PropensitySummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPropensitySummary().then(setData).catch((err) => setError(err.message));
  }, []);

  if (error) return <ErrorState message={error} />;
  if (!data) return <LoadingState />;

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Customer propensity</p>
          <h1>Churn risk workbench</h1>
        </div>
        <button className="primary-button" onClick={exportPropensityCustomers}>
          <Download size={18} />
          Export list
        </button>
      </header>

      <div className="kpi-grid">
        {data.metrics.map((metric) => (
          <KpiCard key={metric.label} metric={metric} />
        ))}
      </div>

      <section className="panel wide">
        <h2>Prioritized customers</h2>
        <PropensityTable customers={data.customers} />
      </section>
    </section>
  );
}
