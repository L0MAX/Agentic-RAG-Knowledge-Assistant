import { type FormEvent, useState } from "react";

import { useAuth } from "../auth/AuthContext";
import { api } from "../api/client";

export function ProfilePage() {
  const { user, refresh } = useAuth();
  const [email, setEmail] = useState(user?.email ?? "");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [notice, setNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (!user) {
    return null;
  }
  const currentUser = user;

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice(null);
    setError(null);
    setSubmitting(true);
    try {
      await api.updateProfile({
        email: email !== currentUser.email ? email : undefined,
        current_password: currentPassword || undefined,
        new_password: newPassword || undefined,
      });
      await refresh();
      setCurrentPassword("");
      setNewPassword("");
      setNotice("Profile updated.");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to update profile.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="panel">
      <p className="eyebrow">Account</p>
      <h2>Profile</h2>
      <p className="lede">Change your email or password. Password changes require your current password.</p>
      <form className="form" onSubmit={onSubmit}>
        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>
        <label>
          Current password
          <input
            type="password"
            autoComplete="current-password"
            value={currentPassword}
            onChange={(event) => setCurrentPassword(event.target.value)}
          />
        </label>
        <label>
          New password
          <input
            type="password"
            autoComplete="new-password"
            value={newPassword}
            onChange={(event) => setNewPassword(event.target.value)}
            minLength={8}
          />
        </label>
        <button type="submit" disabled={submitting}>
          {submitting ? "Saving…" : "Save changes"}
        </button>
      </form>
      {notice ? <p className="notice">{notice}</p> : null}
      {error ? <p className="notice notice-error">{error}</p> : null}
    </section>
  );
}
