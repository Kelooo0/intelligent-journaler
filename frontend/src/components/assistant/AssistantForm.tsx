import { useState } from "react";
import { AssistantResponse } from "../../api/assistantApi";

type AssistantFormProps = {
    onError: (message: string) => void;
    onStart: () => void;
    onChunk: (chunk: string) => void;
}

export default function AssistantForm({
    onError,
    onStart,
    onChunk
}: AssistantFormProps) {
    const [content, setContent] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
            event.preventDefault();
            try {
                setIsLoading(true);
                onStart();

                await AssistantResponse({content}, onChunk)
            } catch (error) {
                onError(
                error instanceof Error
                ? error.message
                : "Failed to retrieve assistant response"
                );

            } finally {
                setIsLoading(false);
            }
        }
    return(
        <form onSubmit={handleSubmit}>
            <textarea placeholder="Ask assistant about your entries..." value={content} onChange={(event) => setContent(event.target.value)} disabled={isLoading}></textarea>
            <button type="submit" disabled={isLoading}>Ask assistant</button>
        </form>
    )
}
