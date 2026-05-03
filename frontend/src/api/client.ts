import { getApiBaseUrl } from "./config";
import { getStoredAccessToken } from "./storage";
import type { ProblemDetailError } from "./types";

function detailToMessage(raw: ProblemDetailError["detail"]): string | null {
  if (typeof raw === "string" && raw.trim()) return raw.trim();
  if (Array.isArray(raw) && raw.length) {
    const parts: string[] = [];
    for (const item of raw) {
      if (typeof item === "string" && item.trim()) parts.push(item.trim());
      else if (item && typeof item === "object" && "msg" in item) {
        const m = (item as { msg?: unknown }).msg;
        if (typeof m === "string" && m.trim()) parts.push(m.trim());
      }
    }
    if (parts.length) return parts.join(". ");
    return null;
  }
  return null;
}

async function parseErrorBody(response: Response): Promise<string> {
  try {
    const data = (await response.json()) as ProblemDetailError & Record<string, unknown>;

    const fromDetail = detailToMessage(data.detail);
    if (fromDetail) return fromDetail;

    const err = data.error;
    if (typeof err === "string" && err.trim()) return err.trim();

    const msg = data.message;
    if (typeof msg === "string" && msg.trim()) return msg.trim();

    return response.statusText || String(response.status);
  } catch {
    return response.statusText || String(response.status);
  }
}

export async function fetchJson<T>(
  path: string,
  init: RequestInit & { auth?: boolean } = {},
): Promise<T> {
  const { auth, headers: initHeaders, ...rest } = init;
  const headers = new Headers(initHeaders);
  if (!headers.has("Content-Type") && rest.body && !(rest.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  if (auth) {
    const t = getStoredAccessToken();
    if (t) headers.set("Authorization", `Bearer ${t}`);
  }
  const url = `${getApiBaseUrl()}${path.startsWith("/") ? path : `/${path}`}`;
  const response = await fetch(url, { ...rest, headers });
  if (!response.ok) {
    throw new Error(await parseErrorBody(response));
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export async function loginForm(username: string, password: string) {
  const body = new URLSearchParams();
  body.set("username", username);
  body.set("password", password);

  const response = await fetch(`${getApiBaseUrl()}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!response.ok) {
    throw new Error(await parseErrorBody(response));
  }
  return response.json() as Promise<{ access_token: string; token_type: string }>;
}
