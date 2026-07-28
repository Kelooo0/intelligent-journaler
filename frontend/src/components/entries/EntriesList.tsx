import { useState } from "react";
import type { Entry } from "../../types/entry";
import { useEffect } from "react";
import { getEntries } from "../../api/entriesApi";

import EntryPreview from "./EntryPreview";

type EntriesListProps = {
    onError: (message: string) => void;
}

export default function EntriesList({
    onError,
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
                    : "Failed to fetch entries."
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

    return (
        <section>
            <h1>Your entries</h1>
            {entries.map((entry) => (<EntryPreview key={entry.id} entry={entry}  /> ))}
        </section>
    )

}
