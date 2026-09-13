import { useEffect, useState } from "react";

import { getChurnSummary } from "../api/churnApi";
import { getPortfolioSegments } from "../api/portfolioApi";
import { BarList } from "../components/charts/BarList";
import { DonutChart } from "../components/charts/DonutChart";
import { LineTrend } from "../components/charts/LineTrend";
import { OutcomeStack } from "../components/charts/OutcomeStack";
import { KpiCard } from "../components/cards/KpiCard";
import { DashboardFilters } from "../components/filters/DashboardFilters";
import { ErrorState } from "../components/states/ErrorState";
import { LoadingState } from "../components/states/LoadingState";
import type { ChurnSummary } from "../types/churn";
import type { DashboardFilters as DashboardFilterValues, SegmentOptions } from "../types/portfolio";

export function ChurnPage() {
  const [data, setData] = useState<ChurnSummary | null>(null);
  const [options, setOptions] = useState<SegmentOptions>({});
  const [filters, setFilters] = useState<DashboardFilterValues>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPortfolioSegments().then(setOptions).catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    setData(null);
    setError(null);
    getChurnSummary(filters).then(setData).catch((err) => setError(err.message));
  }, [filters]);

  if (error) return <ErrorState message={error} />;
  if (!data) return <LoadingState />;

  const recentChurn = data.timeseries.slice(-18);

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Historical churn</p>
          <h1>Churn outcomes and segment pressure</h1>
        </div>
        <span className="data-badge">Site contract episode view</span>
      </header>

      <DashboardFilters options={options} values={filters} onChange={setFilters} />

      <div className="kpi-grid six">
        {data.metrics.map((metric) => (
          <KpiCard key={metric.label} metric={metric} />
        ))}
      </div>

      <div className="spotlight-grid">
        <section className="panel">
          <div className="panel-heading">
            <h2>Churn trend</h2>
            <p>Recent monthly site contracts with drop type Churn.</p>
          </div>
          <LineTrend data={recentChurn} dataKey="churned_sites" stroke="#b3261e" />
        </section>
        <section className="panel">
          <div className="panel-heading">
            <h2>Outcome mix</h2>
            <p>Contract episode outcomes in the current selection.</p>
          </div>
          <DonutChart data={data.outcomes} />
        </section>
      </div>

      <section className="panel wide">
        <div className="panel-heading">
          <h2>Recent monthly outcomes</h2>
          <p>Churn, renewal, TOS, and leakage outcomes over the latest months.</p>
        </div>
        <OutcomeStack data={data.monthly_outcomes} />
      </section>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-heading">
            <h2>Churn by channel</h2>
            <p>Channels associated with churned site contracts.</p>
          </div>
          <BarList data={data.by_channel} />
        </section>
        <section className="panel">
          <div className="panel-heading">
            <h2>Churn by commodity</h2>
            <p>Commodity mix for churned sites.</p>
          </div>
          <BarList data={data.by_commodity} />
        </section>
      </div>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-heading">
            <h2>Churn by sales type</h2>
            <p>Whether churn follows organic, renewal, or TOS sales tagging.</p>
          </div>
          <BarList data={data.by_sales_type} />
        </section>
        <section className="panel">
          <div className="panel-heading">
            <h2>Digital customer flag</h2>
            <p>Churn split by business partner digital adoption.</p>
          </div>
          <BarList data={data.by_digital} />
        </section>
      </div>

      <section className="panel wide">
        <div className="panel-heading">
          <h2>Top agents by churned sites</h2>
          <p>Use as a diagnostic cut alongside channel, cohort, and customer mix.</p>
        </div>
        <BarList data={data.by_agent} />
      </section>
    </section>
  );
}
