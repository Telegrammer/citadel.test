export const TOKEN_STORAGE_KEY = "citadel_access_token";

export function getStoredAccessToken(): string | null {
  return localStorage.getItem(TOKEN_STORAGE_KEY);
}

export function setStoredAccessToken(token: string): void {
  localStorage.setItem(TOKEN_STORAGE_KEY, token);
}

export function clearStoredAccessToken(): void {
  localStorage.removeItem(TOKEN_STORAGE_KEY);
}
