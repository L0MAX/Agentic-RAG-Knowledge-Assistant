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

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }
  return (await response.json()) as T;
}

export const api = {
  getHealth: () => request<HealthResponse>("/health"),
  getApiInfo: () => request<ApiInfoResponse>("/api/v1/"),
};

export { API_BASE_URL };
