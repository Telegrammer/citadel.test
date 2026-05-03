const DEFAULT_BASE = "http://localhost:8000";

export function getApiBaseUrl(): string {
  const fromEnv = import.meta.env.VITE_API_URL;
  const raw =
    typeof fromEnv === "string" && fromEnv.trim() !== ""
      ? fromEnv.trim()
      : DEFAULT_BASE;
  return raw.replace(/\/$/, "");
}
