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
    return (
        <section className="entries-page-list">
            <section className="list-header-container">
                <h1 className="list-header">Your entries</h1>
            </section>
            <section className="entries-list-container">
                <section className="entries-list">
                    {entries.map((entry) => (<EntryPreview key={entry.id} entry={entry}  /> ))}
                    {isLoading && <p className="list-message">Loading...</p>}
                    {entries.length === 0 && <p className="list-message">No entries found.</p>}
                </section>
            </section>
        </section>
    )
}
