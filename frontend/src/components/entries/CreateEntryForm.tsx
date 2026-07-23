import { useState } from "react";
import { createEntry } from "../../api/entriesApi";
import type { Entry } from "../../types/entry";

type CreateEntryProps = {
    onSuccess: (result: Entry) => void;
    onError: (message: string) => void;
}

export default function CreateEntryForm({
    onSuccess,
    onError
}: CreateEntryProps) {
    const [content, setContent] = useState("");
    const [isLoading, setIsLoading] = useState(false);


    async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        try {
            setIsLoading(true);
            onError("");

            const data = await createEntry({ content });
            onSuccess(data);
        } catch (error) {
            onError(
                error instanceof Error
                ? error.message
                : "An unexpected error occured",
            );
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="content">Your entry</label>
            <textarea id="content" value={content} onChange={(event) => setContent(event.target.value)} placeholder="How are you feeling today..." disabled={isLoading}></textarea>
            <button type="submit">{isLoading ? "Adding entry..." : "Add entry"}</button>
        </form>
    );
}
