import { useState } from "react";
import { createEntry } from "../../api/entriesApi";
import { useNavigate } from "react-router";

type CreateEntryFormProps = {
    onError: (message: string) => void;
}

export default function CreateEntryForm({
    onError
}: CreateEntryFormProps) {
    const navigate = useNavigate();
    const [content, setContent] = useState("");
    const [isLoading, setIsLoading] = useState(false);


    async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        try {
            setIsLoading(true);

            await createEntry({ content });
            navigate("/entries", {
                "state": {"message": "Entry added succesfully", "type": "success"}
            });
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
            <button type="submit">{isLoading ? "Adding entry..." : "Add entry"}</button>
        </form>
    );
}
