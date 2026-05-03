import { ROUTES } from "./routes";

export function getApiBaseUrl(): string {
  const raw = import.meta.env.VITE_API_BASE_URL;
  const base =
    typeof raw === "string" && raw.trim() !== "" ? raw.trim() : "http://localhost:8000";
  return base.replace(/\/$/, "");
}

export function getStatusWebSocketUrl(token: string): string {
  const url = new URL(getApiBaseUrl());
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  url.pathname = ROUTES.wsConnectionStatus;
  url.searchParams.set("token", token);
  return url.href;
}
