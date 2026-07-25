import { useState } from "react";
import type { Entry } from "../../types/entry";
import { useEffect } from "react";
import { getEntries } from "../../api/entriesApi";
import { deleteEntry } from "../../api/entriesApi";
import EntryCard from "./EntryCard";

type EntriesListProps = {
    onError: (message: string) => void;
    onDelete: (deleted: boolean) => void;
}

export default function EntriesList({
    onError,
    onDelete
}: EntriesListProps) {
    const [entries, setEntries] = useState<Entry[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function load_entries() {
            try {
                setIsLoading(true);
                onError("");

                const data = await getEntries();
                setEntries(data);
            } catch(error) {
                onError(
                    error instanceof Error
                    ? error.message
                    : "Failed to fetch entries"
                )
                return;
            } finally {
                setIsLoading(false);
            }
        }
        load_entries()
    }, []);

    if(isLoading) {
        return <p>Loading entries...</p>
    }
    if(entries.length === 0) {
        return <p>You don't have any entries yet</p>
    }

    async function handleDelete(id:number) {
        const confirmed = window.confirm("Are you sure you want to delete this entry?");

        if(!confirmed) {
            return;
        }
        try {
            await deleteEntry(id);
            setEntries((entries) =>
            entries.filter((entry) => entry.id !== id),);
            onDelete(true);
        } catch(error) {
            onError(
                error instanceof Error
                ? error.message
                : "Couldn't delete entry"
            );
        }

    }

    return (
        <section>
            <h2>Your entries</h2>
            {entries.map((entry) => (<EntryCard key={entry.id} entry={entry} onDelete={handleDelete} /> ))}
        </section>
    )

}
