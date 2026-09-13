import { useEffect, useState } from "react";

import { getPortfolioSegments, getPortfolioSummary } from "../api/portfolioApi";
import { BarList } from "../components/charts/BarList";
import { DonutChart } from "../components/charts/DonutChart";
import { LineTrend } from "../components/charts/LineTrend";
import { KpiCard } from "../components/cards/KpiCard";
import { DashboardFilters } from "../components/filters/DashboardFilters";
import { ErrorState } from "../components/states/ErrorState";
import { LoadingState } from "../components/states/LoadingState";
import type { DashboardFilters as DashboardFilterValues, PortfolioSummary, SegmentOptions } from "../types/portfolio";

export function PortfolioPage() {
  const [data, setData] = useState<PortfolioSummary | null>(null);
  const [options, setOptions] = useState<SegmentOptions>({});
  const [filters, setFilters] = useState<DashboardFilterValues>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPortfolioSegments().then(setOptions).catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    setData(null);
    setError(null);
    getPortfolioSummary(filters).then(setData).catch((err) => setError(err.message));
  }, [filters]);

  if (error) return <ErrorState message={error} />;
  if (!data) return <LoadingState />;

  const recentSignups = data.signups_by_month.slice(-18);
  const recentStarts = data.active_contract_starts.slice(-18);

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Current portfolio</p>
          <h1>Active customer and site portfolio</h1>
        </div>
        <span className="data-badge">Raw CSV contract episodes</span>
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
            <h2>Active sites by commodity</h2>
            <p>Current contract footprint across electricity, gas, and dual-fuel sites.</p>
          </div>
          <DonutChart data={data.by_commodity} />
        </section>
        <section className="panel">
          <div className="panel-heading">
            <h2>Customer site density</h2>
            <p>Unique site IDs attached to each business partner.</p>
          </div>
          <BarList data={data.site_density} />
        </section>
      </div>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-heading">
            <h2>Active sites by channel</h2>
            <p>Sales channels carrying the current base.</p>
          </div>
          <BarList data={data.by_channel} />
        </section>
        <section className="panel">
          <div className="panel-heading">
            <h2>Active sites by sales type</h2>
            <p>Organic, renewal, and TOS-driven portfolio composition.</p>
          </div>
          <BarList data={data.by_sales_type} />
        </section>
      </div>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-heading">
            <h2>Average monthly billing</h2>
            <p>AMB adoption among active site contracts.</p>
          </div>
          <BarList data={data.by_billing} />
        </section>
        <section className="panel">
          <div className="panel-heading">
            <h2>Plan options</h2>
            <p>Evergreen and surge options represented in the active base.</p>
          </div>
          <div className="split-bars">
            <BarList data={data.by_evergreen} />
            <BarList data={data.by_surge} />
          </div>
        </section>
      </div>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-heading">
            <h2>Business partner signups</h2>
            <p>Recent monthly acquisition volume by original signup date.</p>
          </div>
          <LineTrend data={recentSignups} dataKey="signed_up_customers" stroke="#385f8f" />
        </section>
        <section className="panel">
          <div className="panel-heading">
            <h2>Active contract starts</h2>
            <p>Start months for contracts still active in the portfolio.</p>
          </div>
          <LineTrend data={recentStarts} dataKey="active_contract_starts" stroke="#006b5f" />
        </section>
      </div>
    </section>
  );
}
