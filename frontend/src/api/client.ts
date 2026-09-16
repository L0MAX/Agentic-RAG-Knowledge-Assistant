const TOKEN_KEY = "agentic_rag.access_token";

export type HealthResponse = {
  status: string;
  env: string;
  service: string;
};

export type ApiInfoResponse = {
  name: string;
  version: string;
  env: string;
};

export type User = {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
  user: User;
};

export type KnowledgeBase = {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
};

export type ApiError = {
  code?: string;
  message?: string;
  detail?: unknown;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function storeToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  if (!headers.has("Content-Type") && init.body) {
    headers.set("Content-Type", "application/json");
  }
  const token = getStoredToken();
  if (token && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });
  if (!response.ok) {
    let message = `Request failed: ${response.status} ${response.statusText}`;
    try {
      const payload = (await response.json()) as ApiError;
      if (payload.message) {
        message = payload.message;
      }
    } catch {
      // Keep the status text when the body is not JSON.
    }
    throw new Error(message);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export const api = {
  getHealth: () => request<HealthResponse>("/health"),
  getApiInfo: () => request<ApiInfoResponse>("/api/v1/"),
  register: (email: string, password: string) =>
    request<TokenResponse>("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  login: (email: string, password: string) =>
    request<TokenResponse>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  logout: () => request<void>("/api/v1/auth/logout", { method: "POST" }),
  me: () => request<User>("/api/v1/auth/me"),
  updateProfile: (body: {
    email?: string;
    current_password?: string;
    new_password?: string;
  }) =>
    request<User>("/api/v1/auth/me", {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  listKnowledgeBases: () => request<KnowledgeBase[]>("/api/v1/knowledge-bases"),
  createKnowledgeBase: (name: string, description?: string) =>
    request<KnowledgeBase>("/api/v1/knowledge-bases", {
      method: "POST",
      body: JSON.stringify({ name, description }),
    }),
  deleteKnowledgeBase: (id: string) =>
    request<void>(`/api/v1/knowledge-bases/${id}`, { method: "DELETE" }),
};

export { API_BASE_URL };
