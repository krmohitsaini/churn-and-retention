import { useEffect, useState } from "react";

import { getKpiDefinitions, type KpiDefinition } from "../api/adminApi";
import { ErrorState } from "../components/states/ErrorState";
import { LoadingState } from "../components/states/LoadingState";

export function AdminKpiPage() {
  const [kpis, setKpis] = useState<KpiDefinition[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getKpiDefinitions().then(setKpis).catch((err) => setError(err.message));
  }, []);

  if (error) return <ErrorState message={error} />;
  if (!kpis) return <LoadingState />;

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Admin</p>
          <h1>KPI logic map</h1>
        </div>
      </header>

      <div className="definition-list">
        {kpis.map((kpi) => (
          <article className="definition-row" key={kpi.name}>
            <strong>{kpi.name}</strong>
            <p>{kpi.definition}</p>
            <code>{kpi.module}</code>
          </article>
        ))}
      </div>
    </section>
  );
}
