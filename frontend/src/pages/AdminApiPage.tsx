import { useEffect, useState } from "react";

import { getApiDefinitions, type ApiDefinition } from "../api/adminApi";
import { ErrorState } from "../components/states/ErrorState";
import { LoadingState } from "../components/states/LoadingState";

export function AdminApiPage() {
  const [apis, setApis] = useState<ApiDefinition[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getApiDefinitions().then(setApis).catch((err) => setError(err.message));
  }, []);

  if (error) return <ErrorState message={error} />;
  if (!apis) return <LoadingState />;

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Admin</p>
          <h1>API debug map</h1>
        </div>
      </header>

      <div className="definition-list">
        {apis.map((api) => (
          <article className="definition-row" key={api.path}>
            <span className="method-pill">{api.method}</span>
            <strong>{api.path}</strong>
            <p>{api.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
