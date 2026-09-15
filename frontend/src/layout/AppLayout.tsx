import { NavLink, Outlet } from "react-router-dom";

const links = [
  { to: "/login", label: "Login" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/chat", label: "Chat" },
];

export function AppLayout() {
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
        </nav>
      </header>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
