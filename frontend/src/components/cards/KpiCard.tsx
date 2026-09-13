import type { MetricCard } from "../../types/portfolio";

export function KpiCard({ metric }: { metric: MetricCard }) {
  return (
    <article className="kpi-card">
      <span>{metric.label}</span>
      <strong>{metric.value}</strong>
      {metric.helper ? <small>{metric.helper}</small> : null}
    </article>
  );
}

