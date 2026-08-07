import type { Entry } from "../../types/entry"
import { Link } from "react-router";

type EntryPreviewProps = {
    entry: Entry;
};

export default function EntryPreview({
    entry,
}: EntryPreviewProps) {
    return (
    <article className="preview-container">
        <section className="preview-header-container">
            <h2 className="preview-header">Entry - <time dateTime={entry.created_at}>{new Date(entry.created_at).toLocaleString("en-EN")}</time></h2>
        </section>
        <section className="preview-content-container">
            <p className="preview-content">{entry.content}</p>
        </section>
        <section className="preview-link-container">
            <Link className="preview-link" to={`/entries/${entry.id}/details`}>More...</Link>
        </section>
    </article>
    )
}
