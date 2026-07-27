import { apiRequest } from "./client";
import type { EntryPayload, Entry } from "../types/entry";

export function createEntry(
    payload: EntryPayload,
): Promise<Entry> {
    return apiRequest<Entry>("/entries", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });
}

export function getEntries() {
    return apiRequest<Entry[]>("/entries",{
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
}

export function deleteEntry(id: number): Promise<void> {
    return apiRequest<void>(`/entries/${id}`, {
        method: "DELETE"
    });
}

export function getEntry(id: number): Promise<Entry> {
    return apiRequest<Entry>(`/entries/${id}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
}

export function updateEntry(
    payload: EntryPayload, id: number
): Promise<Entry> {
    return apiRequest<Entry>(`/entries/${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });
}
