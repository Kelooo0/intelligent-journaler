import { useState } from "react";
import { createEntry } from "../../api/entriesApi";
import { useNavigate } from "react-router";
import { updateEntry } from "../../api/entriesApi";

type EntryFormProps = {
    onError: (message: string) => void;
    operation: "create" | "update";
    entryId: number | null;
}

export default function EntryForm({
    onError,
    operation,
    entryId
}: EntryFormProps) {
    const navigate = useNavigate();
    const [content, setContent] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        try {
            setIsLoading(true);

            if(operation === "create") {
                await createEntry({ content });
                navigate("/entries/list", {
                    "state": {"message": "Entry added succesfully", "type": "success"}
                });
            }
            if(operation === "update" && entryId) {
                await updateEntry({ content }, entryId);
                navigate(`/entries/${entryId}/details`, {
                    "state": {"message": "Entry updated succesfully", "type": "success"}
                });
            }

        } catch (error) {
            onError(
            error instanceof Error
            ? error.message
            : "Failed to add entry"
            );

        } finally {
            setIsLoading(false);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="content">Your entry</label>
            <textarea id="content" value={content} onChange={(event) => setContent(event.target.value)} placeholder="How are you feeling today..." disabled={isLoading}></textarea>
            {operation === "create" && <button type="submit">{isLoading ? "Adding entry..." : "Add entry"}</button>}
            {operation === "update" && <button type="submit">{isLoading ? "Updating entry..." : "Update entry"}</button>}
        </form>
    );
}
