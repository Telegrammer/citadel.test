import { getApiBaseUrl } from "./config";
import { ROUTES } from "./routes";
import type { ClaimedVirtualMachine } from "./types";

function detailToMessage(detail: unknown): string | null {
  if (typeof detail === "string" && detail.trim()) return detail.trim();
  if (Array.isArray(detail) && detail.length) {
    const parts: string[] = [];
    for (const item of detail) {
      if (typeof item === "string" && item.trim()) parts.push(item.trim());
      else if (item && typeof item === "object" && item !== null && "msg" in item) {
        const m = (item as { msg?: unknown }).msg;
        if (typeof m === "string" && m.trim()) parts.push(m.trim());
      }
    }
    if (parts.length) return parts.join(". ");
  }
  return null;
}

async function parseError(response: Response): Promise<string> {
  try {
    const data = (await response.json()) as Record<string, unknown>;
    const fromDetail = detailToMessage(data.detail);
    if (fromDetail) return fromDetail;
    if (typeof data.error === "string" && data.error.trim()) return data.error.trim();
    if (typeof data.message === "string" && data.message.trim()) return data.message.trim();
  } catch {
  }
  return response.statusText || `HTTP ${response.status}`;
}

export async function claimVirtualMachine(
  activationKey: string,
): Promise<ClaimedVirtualMachine> {
  const response = await fetch(`${getApiBaseUrl()}${ROUTES.virtualMachinesClaim}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ activation_key: activationKey }),
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as ClaimedVirtualMachine;
}
