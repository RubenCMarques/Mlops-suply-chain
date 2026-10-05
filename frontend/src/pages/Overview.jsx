import { useEffect, useState } from 'react';
import { ArrowUpRight, Database, GitBranch, Package, RefreshCw, Server } from 'lucide-react';
import Status from '../components/Status.jsx';
import { getSystemStatus } from '../services/api.js';

export default function Overview() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(true);
  const [refresh, setRefresh] = useState(0);
  const [checkedAt, setCheckedAt] = useState(null);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(false);
    getSystemStatus(controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) {
          setData(result);
          setCheckedAt(new Date());
        }
      })
      .catch(() => {
        if (!controller.signal.aborted) {
          setData(null);
          setError(true);
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [refresh]);

  return (
    <>
      <header className="topbar">
        <a className="brand" href="/"><Package size={24} />Supply Chain</a>
        <span className="workspace">MLOps workspace</span>
        <span className="environment">{data?.environment || 'Workspace'}</span>
      </header>
      <main>
        <div className="page-heading">
          <div><p className="eyebrow">WORKSPACE</p><h1>Overview</h1></div>
          <div className="actions">
            <a className="text-link" href="/docs" target="_blank" rel="noreferrer">API reference<ArrowUpRight size={16} /></a>
            <button className="icon-button" type="button" title="Refresh status" aria-label="Refresh status" disabled={loading} onClick={() => setRefresh((value) => value + 1)}>
              <RefreshCw size={18} className={loading ? 'spin' : ''} />
            </button>
          </div>
        </div>

        {error && <div role="alert" className="error">The backend is unavailable. Status could not be retrieved.</div>}

        <section aria-labelledby="connections-title" aria-busy={loading}>
          <div className="section-heading"><h2 id="connections-title">Connections</h2><span className="muted" role="status">{loading ? 'Checking...' : checkedAt && !error ? `Checked ${checkedAt.toLocaleTimeString()}` : 'Not connected'}</span></div>
          <div className="connection-row">
            <Server className="service-icon" size={20} />
            <div><h3>Backend API</h3><p className="muted">FastAPI</p></div>
            <Status tone={loading ? 'neutral' : error ? 'error' : 'success'}>{loading ? 'Checking' : error ? 'Unavailable' : 'Connected'}</Status>
          </div>
          <div className="connection-row">
            <Database className="service-icon" size={20} />
            <div><h3>Feature store</h3><p className="muted">Hopsworks</p></div>
            <div className="connection-state"><Status tone={data && !loading ? 'warning' : 'neutral'}>{loading ? 'Checking' : !data ? 'Unknown' : data.feature_store.configured ? 'Configured' : 'Not configured'}</Status>{data?.feature_store.configured && !loading && <small>Connection not verified</small>}</div>
          </div>
        </section>

        <section aria-labelledby="pipelines-title">
          <div className="section-heading"><h2 id="pipelines-title">Pipelines</h2><span className="muted">Kedro</span></div>
          <div className="table-scroll">
            <table>
              <thead><tr><th>Name</th><th>Nodes</th><th>Definition</th></tr></thead>
              <tbody>
                {data?.pipelines.map((pipeline) => <tr key={pipeline.name}><td><span className="pipeline-name"><GitBranch size={16} />{pipeline.name}</span></td><td>{pipeline.nodes}</td><td><Status>Registered</Status></td></tr>)}
                {!data && <tr><td colSpan="3" className="empty">{loading ? 'Loading pipelines...' : 'Pipeline status unavailable'}</td></tr>}
              </tbody>
            </table>
          </div>
        </section>
      </main>
      <footer><span>Supply Chain</span><span>Development workspace</span></footer>
    </>
  );
}
