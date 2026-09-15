import { useEffect, useState } from "react";

import { API_BASE_URL, api, type ApiInfoResponse, type HealthResponse } from "../api/client";

export function DashboardPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [info, setInfo] = useState<ApiInfoResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const [healthResponse, infoResponse] = await Promise.all([
          api.getHealth(),
          api.getApiInfo(),
        ]);
        if (!cancelled) {
          setHealth(healthResponse);
          setInfo(infoResponse);
        }
      } catch (cause) {
        if (!cancelled) {
          setError(cause instanceof Error ? cause.message : "Unable to reach the API.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section className="panel">
      <p className="eyebrow">Workspace</p>
      <h2>Dashboard</h2>
      <p className="lede">
        Knowledge bases, document processing, and conversations will land here. For now this
        page confirms the frontend can reach the backend.
      </p>
      <dl className="meta-grid">
        <div>
          <dt>API base</dt>
          <dd>{API_BASE_URL}</dd>
        </div>
        <div>
          <dt>Backend status</dt>
          <dd>{loading ? "Checking…" : health?.status ?? "unavailable"}</dd>
        </div>
        <div>
          <dt>Environment</dt>
          <dd>{info?.env ?? health?.env ?? "—"}</dd>
        </div>
        <div>
          <dt>API version</dt>
          <dd>{info?.version ?? "—"}</dd>
        </div>
      </dl>
      {error ? (
        <p className="notice notice-error">
          {error} Start the backend on port 8000, or use Docker Compose.
        </p>
      ) : null}
    </section>
  );
}
