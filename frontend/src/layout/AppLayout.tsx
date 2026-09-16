import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";

export function AppLayout() {
  const { user, logout } = useAuth();

  const links = user
    ? [
        { to: "/dashboard", label: "Dashboard" },
        { to: "/chat", label: "Chat" },
        { to: "/profile", label: "Profile" },
      ]
    : [
        { to: "/login", label: "Login" },
        { to: "/register", label: "Register" },
      ];

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true" />
          <div>
            <p className="brand-kicker">Knowledge Assistant</p>
            <h1>Agentic RAG</h1>
          </div>
        </div>
        <nav className="nav">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              {link.label}
            </NavLink>
          ))}
          {user ? (
            <button type="button" className="nav-link ghost-nav" onClick={() => void logout()}>
              Log out
            </button>
          ) : null}
        </nav>
      </header>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
