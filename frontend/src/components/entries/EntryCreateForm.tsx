import { useState } from "react";
import { createEntry } from "../../api/entriesApi";
import { useNavigate } from "react-router";
import "../../pages/EntryOp.css";

type EntryFormProps = {
    onError: (message: string) => void;
}

export default function EntryCreateForm({
    onError,
}: EntryFormProps) {
    const navigate = useNavigate();
    const [content, setContent] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        try {
            setIsLoading(true);

            await createEntry({ content });
            navigate("/entries/list", {
                "state": {"message": "Entry added succesfully.", "type": "success"}
            });
        } catch (error) {
            onError(
            error instanceof Error
            ? error.message
            : "Failed to add entry."
            );

        } finally {
            setIsLoading(false);
        }
    }

    return (
        <form onSubmit={handleSubmit} className="entry-form">
            <textarea id="content" className="entry-form-text" value={content} onChange={(event) => setContent(event.target.value)} placeholder="How are you feeling today..." disabled={isLoading}></textarea>
            <button type="submit" className="entry-form-submit" disabled={isLoading}>{isLoading ? "Adding..." : "Add"}</button>
        </form>
    );
}
