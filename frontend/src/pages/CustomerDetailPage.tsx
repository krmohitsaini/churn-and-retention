import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getCustomerDetail } from "../api/customerApi";
import { ErrorState } from "../components/states/ErrorState";
import { LoadingState } from "../components/states/LoadingState";
import type { CustomerDetail } from "../types/customer";

export function CustomerDetailPage() {
  const { customerId = "" } = useParams();
  const [data, setData] = useState<CustomerDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCustomerDetail(customerId).then(setData).catch((err) => setError(err.message));
  }, [customerId]);

  if (error) return <ErrorState message={error} />;
  if (!data) return <LoadingState />;

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Customer detail</p>
          <h1>{String(data.customer.customer_id)}</h1>
        </div>
        <Link className="secondary-button" to="/propensity">
          Back to propensity
        </Link>
      </header>

      <div className="content-grid">
        <section className="panel">
          <h2>Profile</h2>
          <dl className="detail-list">
            {Object.entries(data.customer).map(([key, value]) => (
              <div key={key}>
                <dt>{key.replaceAll("_", " ")}</dt>
                <dd>{String(value)}</dd>
              </div>
            ))}
          </dl>
        </section>
        <section className="panel">
          <h2>Propensity</h2>
          <dl className="detail-list">
            {Object.entries(data.propensity ?? {}).map(([key, value]) => (
              <div key={key}>
                <dt>{key.replaceAll("_", " ")}</dt>
                <dd>{String(value)}</dd>
              </div>
            ))}
          </dl>
        </section>
      </div>

      <section className="panel wide">
        <h2>Interactions</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Channel</th>
                <th>Type</th>
                <th>Sentiment</th>
                <th>Issue</th>
                <th>Resolved</th>
              </tr>
            </thead>
            <tbody>
              {data.interactions.map((interaction) => (
                <tr key={String(interaction.interaction_id)}>
                  <td>{String(interaction.interaction_date)}</td>
                  <td>{String(interaction.channel)}</td>
                  <td>{String(interaction.interaction_type)}</td>
                  <td>{String(interaction.sentiment)}</td>
                  <td>{String(interaction.issue_category)}</td>
                  <td>{String(interaction.resolved_flag)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}
