import { type FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [notice, setNotice] = useState<string | null>(null);

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!email || !password) {
      setNotice("Enter an email and password to continue to the placeholder dashboard.");
      return;
    }
    setNotice("Authentication is not implemented yet (Phase 3). Opening the dashboard shell.");
    window.setTimeout(() => navigate("/dashboard"), 600);
  }

  return (
    <section className="panel auth-panel">
      <p className="eyebrow">Phase 1 placeholder</p>
      <h2>Sign in</h2>
      <p className="lede">
        Registration, JWT sessions, and protected routes arrive in Phase 3. This screen
        establishes the authentication flow layout.
      </p>
      <form className="form" onSubmit={onSubmit}>
        <label>
          Email
          <input
            type="email"
            autoComplete="username"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
          />
        </label>
        <label>
          Password
          <input
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="••••••••"
          />
        </label>
        <button type="submit">Continue</button>
      </form>
      {notice ? <p className="notice">{notice}</p> : null}
    </section>
  );
}
