import { type FormEvent, useEffect, useState } from "react";

import { api, type KnowledgeBase } from "../api/client";
import { useAuth } from "../auth/AuthContext";

export function DashboardPage() {
  const { user } = useAuth();
  const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBase[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try {
      setKnowledgeBases(await api.listKnowledgeBases());
      setError(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to load knowledge bases.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function onCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      await api.createKnowledgeBase(name, description || undefined);
      setName("");
      setDescription("");
      await load();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to create knowledge base.");
    }
  }

  async function onDelete(id: string) {
    try {
      await api.deleteKnowledgeBase(id);
      await load();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to delete knowledge base.");
    }
  }

  return (
    <section className="panel">
      <p className="eyebrow">Workspace</p>
      <h2>Dashboard</h2>
      <p className="lede">Signed in as {user?.email}. Create a knowledge base to hold documents.</p>
      <form className="form" onSubmit={onCreate}>
        <label>
          Name
          <input value={name} onChange={(event) => setName(event.target.value)} required maxLength={200} />
        </label>
        <label>
          Description
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            rows={3}
            maxLength={4000}
          />
        </label>
        <button type="submit">Create knowledge base</button>
      </form>
      {loading ? <p className="lede">Loading knowledge bases…</p> : null}
      {error ? <p className="notice notice-error">{error}</p> : null}
      <ul className="kb-list">
        {knowledgeBases.map((item) => (
          <li key={item.id}>
            <div>
              <strong>{item.name}</strong>
              <p>{item.description || "No description"}</p>
            </div>
            <button type="button" className="ghost" onClick={() => void onDelete(item.id)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
