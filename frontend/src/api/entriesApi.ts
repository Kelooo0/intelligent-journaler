import { apiRequest } from "./client";
import type { CreateEntryPayload, Entry } from "../types/entry";

export function createEntry(
    payload: CreateEntryPayload,
): Promise<Entry> {
    return apiRequest<Entry>("/entries", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });
}
