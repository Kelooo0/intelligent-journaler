import { getErrorMessage } from "./getErrorMessage";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const token = localStorage.getItem("access_token");
  const headers = new Headers(options.headers);

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    if (token) {
      localStorage.removeItem("access_token");
      sessionStorage.setItem(
        "state",
        JSON.stringify({
          message: "Session expired. Please log in again.",
          type: "info",
        }),
      );
      window.location.href = "/";
      throw new Error("Session expired.");
    }
  }

  if (response.status === 204) {
    return undefined as T;
  }

  if (!response.ok) {
    const message = await response.text();
    const fallback = `A request error occured: ${response.status}`;
    const final_message = getErrorMessage(message, fallback);

    throw new Error(final_message);
  }
  return response.json() as Promise<T>;
}
