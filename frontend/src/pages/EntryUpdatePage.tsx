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
    const entry_id = Number(id)
    const [entry, setEntry] = useState<Entry>();
    const [isLoading, setIsLoading] = useState(false);

    async function validateEntry(): Promise<void> {
        try {
            setIsLoading(true);

            if(!entry_id) {
                navigate("/entries/list", {
                    "state": {"message": "Entry not found", "type": "error"}
                });
            }
            const entryData = await getEntry(entry_id);
            setEntry(entryData);
        } catch (error) {
            navigate("/entries/list", {
                "state": {"message": "Entry not found", "type": "error"}
            });
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
