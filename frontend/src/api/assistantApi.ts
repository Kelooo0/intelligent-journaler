import type { UserQuery } from "../types/assistant";
import { getErrorMessage } from "./getErrorMessage";

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

    if(response.status === 401) {
        if(token) {
            localStorage.removeItem("access_token");
            sessionStorage.setItem("state", JSON.stringify({"message": "Session expired. Please log in again.", "type": "info"}));
            window.location.href = "/";
            throw new Error("Session expired.");
        }
    }

    if(!response.ok) {
        const message = await response.text();
        const fallback = `A request error occured: ${response.status}`;
        const final_message = getErrorMessage(message, fallback);

        throw new Error(
            final_message,
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
