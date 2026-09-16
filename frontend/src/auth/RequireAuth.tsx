import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";

export function RequireAuth() {
  const { user, ready } = useAuth();
  if (!ready) {
    return <section className="panel">Loading session…</section>;
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
}
