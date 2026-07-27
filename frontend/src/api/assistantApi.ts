
import type { UserQuery } from "../types/assistant";

const API_URL = "http://localhost:8000";

export async function AssistantResponse(
    content: UserQuery,
    onChunk: (chunk: string) => void
): Promise<void> {
    const token = localStorage.getItem("access_token");

    const response = await fetch(`${API_URL}/assistant`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...(token
            ? { Authorization: `Bearer ${token}` }
            : {}),
        },
        body: JSON.stringify(content)
    });

    if(!response.ok) {
        const ErrorData = await response.json().catch(() => null);

        throw new Error(
            ErrorData?.detail ?? `Request failed: ${response.status}`,
        );
    }

    if(!response.body) {
        throw new Error("Response stream unavailable");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    while (true) {
        const { value, done } = await reader.read();

        if(done) {
            break;
        }
        const chunk = decoder.decode(value, {stream: true});
        onChunk(chunk)
    }
 }
