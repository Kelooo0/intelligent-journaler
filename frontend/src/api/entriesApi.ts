import { apiRequest } from "./client";
import type { EntryPayload, Entry, getEntriesPayload } from "../types/entry";

export function createEntry(payload: EntryPayload): Promise<Entry> {
  return apiRequest<Entry>("/entries", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function getEntries(payload: getEntriesPayload): Promise<Entry[]> {
  const params = new URLSearchParams();
  if (payload.start_date) {
    params.set("start_date", payload.start_date);
  }
  if (payload.end_date) {
    params.set("end_date", payload.end_date);
  }
  if (payload.tags && payload.tags.length > 0) {
    payload.tags.forEach((tag) => {
      params.append("tags", tag);
    });
  }
  const query = params.toString();

  return apiRequest<Entry[]>(`/entries${query ? `?${query}` : ""}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export function deleteEntry(id: number): Promise<void> {
  return apiRequest<void>(`/entries/${id}`, {
    method: "DELETE",
  });
}

export function getEntry(id: number): Promise<Entry> {
  return apiRequest<Entry>(`/entries/${id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export function updateEntry(payload: EntryPayload, id: number): Promise<Entry> {
  return apiRequest<Entry>(`/entries/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
