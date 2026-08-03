import EntryUpdateForm from "../components/entries/EntryUpdateForm";
import { useState } from "react"
import { useParams } from "react-router";
import { useEffect } from "react";
import { useNavigate } from "react-router";
import { getEntry } from "../api/entriesApi";
import type { Entry } from "../types/entry";
import "./EntryOp.css";

export default function EntryUpdatePage() {
    const navigate = useNavigate();
    const [error, setError] = useState("");
    const { id } = useParams<{ id: string }>();
    const entry_id = Number(id);
    const [entry, setEntry] = useState<Entry>();
    const [isLoading, setIsLoading] = useState(false);

    async function validateEntry(): Promise<void> {
        try {
            setIsLoading(true);

            if(!Number.isInteger(entry_id) || entry_id < 0) {
                navigate("/entries/list", {
                    replace: true, "state": {"message": "Invalid entry ID", "type": "error"}
                });

                return;
            }
            const entryData = await getEntry(entry_id);
            setEntry(entryData);
        } catch (error) {
            const message =
                error instanceof Error
                ? error.message
                : "Failed to fetch entry details."

            navigate("/entries/list", {
                replace: true, "state": {"message": message, "type": "error"}
            });
            return;
        } finally {
            setIsLoading(false);
        }

    }

    useEffect(() => {
        void validateEntry();
    }, []);

    if(isLoading) {
        return (
            <main className="entry-op-main">
                <section className="entry-op-header">
                    <h1>Loading...</h1>
                </section>
            </main>
        )
    }

    return (
        <main className="entry-op-main">
            <section className="entry-op-header">
                <h1>Entry #{entry && entry.id}</h1>
            </section>
            <section className="entry-form-container">
                {entry && <EntryUpdateForm onError={setError} entry={entry}/> }
            </section>
            <section className="entry-op-msgs">
                {error && <p role="alert">{error}</p>}
            </section>
        </main>
    )
}
