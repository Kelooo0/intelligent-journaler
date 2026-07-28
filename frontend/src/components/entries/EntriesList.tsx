import type { Entry } from "../../types/entry";
import EntryPreview from "./EntryPreview";

type EntriesListProps = {
    entries: Entry[];
    isLoading: boolean;
}

export default function EntriesList({
    entries,
    isLoading
}: EntriesListProps) {
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
