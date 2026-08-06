import { useState } from "react";
import { AssistantResponse } from "../../api/assistantApi";

type AssistantFormProps = {
    onError: (message: string) => void;
    onStart: () => void;
    onChunk: (chunk: string) => void;
    onSuccess: () => Promise<void>;
    onLoading: (arg0: boolean) => void;
    loading: boolean;
}

export default function AssistantForm({
    onError,
    onStart,
    onChunk,
    onSuccess,
    onLoading,
    loading,
}: AssistantFormProps) {
    const [content, setContent] = useState("");


    async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
            event.preventDefault();
            try {
                onLoading(true);
                onStart();

                await AssistantResponse({content}, onChunk)
                onSuccess();
            } catch (error) {
                onError(
                error instanceof Error
                ? error.message
                : "Failed to retrieve assistant response"
                );

            } finally {
                onLoading(false);
            }
        }
    return(
        <form  className="assistant-form" onSubmit={handleSubmit}>
            <textarea className="assistant-text" placeholder="Ask assistant about your entries..." value={content} onChange={(event) => setContent(event.target.value)} disabled={loading}></textarea>
            <button className="assistant-submit" type="submit" disabled={loading}>Ask</button>
        </form>
    )
}
