import type { Entry } from "../../types/entry";
import EntryPreview from "./EntryPreview";

type EntriesListProps = {
  entries: Entry[];
  isLoading: boolean;
};

export default function EntriesList({ entries, isLoading }: EntriesListProps) {
  return (
    <section className="entries-page-list">
      <section className="list-header-container">
        <h1 className="list-header">Your entries</h1>
      </section>
      <section className="entries-list-container">
        <section className="entries-list">
          {isLoading ? (
            <section className="list-message-container">
              <p className="list-message">Loading...</p>
            </section>
          ) : entries.length === 0 ? (
            <section className="list-message-container">
              <p className="list-message">No entries found.</p>
            </section>
          ) : (
            entries.map((entry) => (
              <EntryPreview key={entry.id} entry={entry} />
            ))
          )}
        </section>
      </section>
    </section>
  );
}
